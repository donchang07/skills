"""형상·고정구 검사 (시연용 대역) — SC-02 고정구 충돌, SC-04 가공 후 형상과 STEP 모델 비교.
2.5D 높이맵 방식: 위에서 본 격자마다 남은 소재의 윗면 높이를 계산합니다.
평엔드밀·정면 밀링·드릴·리머·탭 하공은 원판으로 깎고, 모따기·센터 드릴·탭·백 모따기 공구는 형상 비교에서 제외합니다(0.6mm 경계 띠 안).
실제 DN Virtual Simulator가 아닙니다.
사용법: python3 sim_check.py OP10.nc OP20.nc SYN-BRK-0101.step
"""
import sys, json, math, re
import numpy as np

RES = 0.25
X0, X1, Y0, Y1 = -10.0, 130.0, -10.0, 90.0
NX, NY = int((X1 - X0) / RES), int((Y1 - Y0) / RES)
gx = X0 + (np.arange(NX) + 0.5) * RES
gy = Y0 + (np.arange(NY) + 0.5) * RES
GX, GY = np.meshgrid(gx, gy, indexing="ij")

# 공구 표: 번호 → (반지름, 형상 비교에 쓰는지)
TOOLS = {1: (25.0, True), 2: (5.0, True), 3: (4.0, True), 4: (5.0, False), 5: (3.9, True), 6: (4.01, True),
         7: (3.0, False), 8: (2.5, True), 9: (3.0, False), 10: (3.5, False)}

# 고정구(직육면체: x1,x2,y1,y2,z1,z2). 셋업마다 G54 좌표
FIXTURES = {
    "OP10": {"바이스 고정 조": (-40, 160, -40, -2.5, -60, -19.5), "바이스 이동 조": (-40, 160, 82.5, 120, -60, -19.5)},
    "OP20": {"바이스 고정 조": (-40, 160, -40, 0, -40, 14), "바이스 이동 조": (-40, 160, 80, 120, -40, 14),
             "평행 블록 1": (-2, 122, 22, 32, -40, 0), "평행 블록 2": (-2, 122, 48, 58, -40, 0),
             "X 스토퍼": (-8, 0, 35, 45, 3, 10)},
}


def moves(fn):
    """NC를 읽어 (공구, 시작점, 끝점, 절삭 여부, 행) 목록으로"""
    pos = [0.0, 0.0, 100.0]; mode = 0; tool = None; cyc = None; R = Zc = None; init = 100.0; ret = 98
    out = []
    for ln, raw in enumerate(open(fn), 1):
        t = re.sub(r"\(.*?\)", "", raw).strip()
        if not t or t == "%": continue
        w = {}; gs = []
        for word in t.split():
            L, v = word[0], float(word[1:])
            if L == "G": gs.append(v)
            else: w[L] = v
        if 91 in gs or 28 in gs: continue
        for g in gs:
            if g in (0, 1, 2, 3): mode = int(g); cyc = None
            elif g in (81, 82, 83, 84, 85):
                if cyc != g: init = pos[2]; R = Zc = None
                cyc = g
            elif g == 80: cyc = None
            elif g in (98, 99): ret = int(g)
        if w.get("M") == 6: tool = int(w["T"])
        if not any(k in w for k in "XYZ"): continue
        tgt = [w.get("X", pos[0]), w.get("Y", pos[1]), w.get("Z", pos[2])]
        if cyc:
            R = w.get("R", R); Zc = w.get("Z", Zc)
            a = [tgt[0], tgt[1], pos[2]]; out.append((tool, pos[:], a, False, ln))
            b = [tgt[0], tgt[1], R]; out.append((tool, a, b, False, ln))
            c = [tgt[0], tgt[1], Zc]; out.append((tool, b, c, True, ln))
            d = [tgt[0], tgt[1], init if ret == 98 else R]; out.append((tool, c, d, False, ln))
            pos = d; continue
        if mode in (2, 3):
            cx, cy = pos[0] + w.get("I", 0), pos[1] + w.get("J", 0)
            r = math.hypot(pos[0] - cx, pos[1] - cy)
            a0 = math.atan2(pos[1] - cy, pos[0] - cx); a1 = math.atan2(tgt[1] - cy, tgt[0] - cx)
            d = (a1 - a0) if mode == 3 else (a0 - a1)
            while d <= 1e-9: d += 2 * math.pi
            n = max(8, int(r * d / 0.2)); prev = pos[:]
            for k in range(1, n + 1):
                ang = a0 + (d * k / n if mode == 3 else -d * k / n)
                p = [cx + r * math.cos(ang), cy + r * math.sin(ang), pos[2] + (tgt[2] - pos[2]) * k / n]
                out.append((tool, prev, p, True, ln)); prev = p
            pos = tgt; continue
        out.append((tool, pos[:], tgt, mode == 1, ln)); pos = tgt
    return out


def samples(a, b, step=0.2):
    n = max(1, int(math.dist(a, b) / step))
    for k in range(n + 1):
        f = k / n
        yield a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f


def simulate(fn, H, fixtures):
    hits = {}
    masks = {}
    for tool, a, b, cutting, ln in moves(fn):
        r, shapes = TOOLS[tool]
        for x, y, z in samples(a, b, 0.2 if cutting else 1.0):
            for name, (x1, x2, y1, y2, z1, z2) in fixtures.items():
                if z < z2 and z + 80 > z1:
                    dx = max(x1 - x, 0, x - x2); dy = max(y1 - y, 0, y - y2)
                    if math.hypot(dx, dy) < r:
                        hits.setdefault((name, tool), ln)
            if cutting and shapes:
                i0, i1 = int((x - r - X0) / RES), int((x + r - X0) / RES) + 2
                j0, j1 = int((y - r - Y0) / RES), int((y + r - Y0) / RES) + 2
                i0, j0 = max(i0, 0), max(j0, 0); i1, j1 = min(i1, NX), min(j1, NY)
                sub = (GX[i0:i1, j0:j1] - x) ** 2 + (GY[i0:i1, j0:j1] - y) ** 2 <= r * r
                blk = H[i0:i1, j0:j1]
                blk[sub] = np.minimum(blk[sub], z)
    return hits


def step_heightmap(step):
    import cadquery as cq
    shape = cq.importers.importStep(step).val()
    vs, tris = shape.tessellate(0.005, 0.05)
    V = np.array([[v.x, v.y, v.z] for v in vs]); E = np.full((NX, NY), -np.inf)
    for t in tris:
        p = V[list(t)]
        (ax_, ay, az), (bx, by, bz), (cx, cy, cz) = p
        den = (by - cy) * (ax_ - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-12: continue  # 수직면
        i0, i1 = max(int((min(ax_, bx, cx) - X0) / RES) - 1, 0), min(int((max(ax_, bx, cx) - X0) / RES) + 2, NX)
        j0, j1 = max(int((min(ay, by, cy) - Y0) / RES) - 1, 0), min(int((max(ay, by, cy) - Y0) / RES) + 2, NY)
        X, Y = GX[i0:i1, j0:j1], GY[i0:i1, j0:j1]
        l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den
        l2 = ((cy - ay) * (X - cx) + (ax_ - cx) * (Y - cy)) / den
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9)
        z = l1 * az + l2 * bz + l3 * cz
        blk = E[i0:i1, j0:j1]
        blk[ins] = np.maximum(blk[ins], z[ins])
    return E


def band(E, width=0.6):
    """기대 높이가 바뀌는 경계에서 width 안의 격자(이산화·모따기 영역) 표시"""
    k = int(math.ceil(width / RES)); B = np.zeros_like(E, dtype=bool)
    Ef = np.where(np.isfinite(E), E, -999)
    for di in range(-k, k + 1):
        for dj in range(-k, k + 1):
            if di * di + dj * dj > k * k: continue
            S = np.roll(np.roll(Ef, di, 0), dj, 1)
            B |= np.abs(S - Ef) > 1e-6
    return B


def judge(H, E, part_mask, allow_deeper=None, tol=0.01):
    B = band(np.where(part_mask, E, 1e9))
    m = part_mask & ~B
    thru = m & ~np.isfinite(E)
    solid = m & np.isfinite(E)
    under = int(((H > E + tol) & solid).sum()) + int((thru & (H > 0)).sum())
    over_mask = (H < E - tol) & solid
    if allow_deeper is not None: over_mask &= ~allow_deeper
    over = int(over_mask.sum())
    return under, over, int(m.sum())


def main(op10, op20, step):
    report = {}
    inside = (GX > 0) & (GX < 120) & (GY > 0) & (GY < 80)
    stock = (GX > -2.5) & (GX < 122.5) & (GY > -2.5) & (GY < 82.5)

    # OP10: 윗면 = 완성될 A면(Z0), 외곽 밖은 Z-17까지 제거
    H = np.where(stock, 2.5, -100.0)
    hits = simulate(op10, H, FIXTURES["OP10"])
    E = np.where(inside, 0.0, -17.0)
    B = band(E)
    under = int(((H > E + 0.01) & stock & ~B).sum()); over = int(((H < E - 0.01) & inside & ~B).sum())
    report["OP10"] = {"fixture_collisions": [f"{n} (T{t}, {l}행)" for (n, t), l in hits.items()], "undercut_cells": under, "overcut_cells": over}

    # OP20: 윗면 높이맵을 STEP 모델 윗면과 비교
    H = np.where(stock, 22.5, -100.0)
    hits = simulate(op20, H, FIXTURES["OP20"])
    E = step_heightmap(step)
    taps = np.zeros_like(inside)
    for x, y in [(60, 8), (60, 72)]:
        taps |= (GX - x) ** 2 + (GY - y) ** 2 <= 2.5 ** 2
    under, over, n = judge(H, E, inside, allow_deeper=taps & (H >= 3.0))
    outside_ok = int(((H > 17.0) & stock & ~inside & ~band(np.where(inside, 1.0, 0.0))).sum())
    feats = {}
    for name, (x, y), rr, want in [("포켓 중심 바닥", (60, 40), 0, 14.0), ("포켓 모서리 근처 바닥(36,26)", (36, 26), 0, 14.0),
                                   ("윗면(5,40)", (5, 40), 0, 20.0)]:
        i, j = int((x - X0) / RES), int((y - Y0) / RES); feats[name] = {"sim": round(float(H[i, j]), 3), "model": want}
    for x, y in [(15, 12), (105, 12), (15, 68), (105, 68)]:
        i, j = int((x - X0) / RES), int((y - Y0) / RES); feats[f"⌀8 홀 ({x},{y}) 바닥"] = {"sim": round(float(H[i, j]), 3), "model": "관통(≤0)"}
    for x, y in [(60, 8), (60, 72)]:
        i, j = int((x - X0) / RES), int((y - Y0) / RES); feats[f"M6 하공 ({x},{y}) 바닥"] = {"sim": round(float(H[i, j]), 3), "model": "≤8 (탭 깊이 12)"}
    report["OP20"] = {"fixture_collisions": [f"{n} (T{t}, {l}행)" for (n, t), l in hits.items()],
                      "compared_cells": n, "undercut_cells": under, "overcut_cells": over,
                      "flange_left_cells": outside_ok, "features": feats}
    ok = all(not report[k]["fixture_collisions"] and report[k]["undercut_cells"] == 0 and report[k]["overcut_cells"] == 0 for k in report) and outside_ok == 0
    report["result"] = "합격" if ok else "불합격"
    report["note"] = "시연용 대역 형상 검사(격자 0.25mm, 경계 0.6mm 띠 제외, 허용 0.01mm). 실제 DN Virtual Simulator 결과가 아닙니다."
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
