"""SYN-BRK-0101 가공 PRD v1.1의 공정표를 그대로 NC 코드로 옮깁니다 (OP10, OP20).
좌표: G54 원점 = 기준 B(X0)·C(Y0)·A(Z0) 교점. OP10은 뒤집힌 상태라 Z0 = 완성될 A면.
공구 경로는 공구 중심 기준(공구 지름 보정 G41/G42 미사용).
"""
from shapely.geometry import Polygon, box, LineString
from shapely.geometry.polygon import orient

PART = Polygon([(0.5, 0), (119.5, 0), (120, 0.5), (120, 79.5), (119.5, 80), (0.5, 80), (0, 79.5), (0, 0.5)])  # 수직 모서리 C0.5
POCKET = box(35, 25, 85, 55).buffer(5, quad_segs=16)  # 60×40, 모서리 R5
HOLES8 = [(15, 12), (105, 12), (15, 68), (105, 68)]
TAPS = [(60, 8), (60, 72)]

def f3(v):
    t = f"{v:.3f}".rstrip("0")
    return "0." if t in ("0.", "-0.") else t


def ring(poly, clockwise):
    p = orient(poly, sign=-1.0 if clockwise else 1.0)
    return list(p.exterior.coords)


def start_at(coords, pt):
    """닫힌 경로를 pt에 가장 가까운 점에서 시작하도록 회전"""
    pts = coords[:-1]
    k = min(range(len(pts)), key=lambda i: (pts[i][0] - pt[0]) ** 2 + (pts[i][1] - pt[1]) ** 2)
    pts = pts[k:] + pts[:k]
    return pts + [pts[0]]


class NC:
    def __init__(self, oname, title, stock_top):
        self.l = ["%", f"{oname} ({title})", "(SYNTHETIC NC FOR REHEARSAL - NOT FOR REAL MACHINE)",
                  f"(STOCK TOP Z{stock_top})", "G21 G17 G40 G49 G80 G90"]

    def add(self, *s): self.l += list(s)

    def tool(self, op, t, desc, s, x, y, h_z=50):
        self.add(f"(OPERATION {op})", f"T{t} M6 ({desc})", f"G0 G90 G54 X{f3(x)} Y{f3(y)} S{s} M3", f"G43 H{t} Z{h_z}. M8")

    def end_tool(self):
        if self.l[-1] != "G0 Z50.": self.add("G0 Z50.")
        self.add("M9", "M5", "G91 G28 Z0.", "G90")

    def path(self, pts, z_cut, feed, lead_from, z_clear=50.0):
        x0, y0 = lead_from
        self.add(f"G0 X{f3(x0)} Y{f3(y0)}", f"G0 Z{f3(z_cut + 5)}", f"G1 Z{f3(z_cut)} F{feed}")
        for x, y in pts:
            self.add(f"G1 X{f3(x)} Y{f3(y)}")
        self.add(f"G1 X{f3(x0)} Y{f3(y0)}")

    def face(self, z, feed):
        ys = [15, 50, 75]
        self.add(f"G0 X-30. Y{ys[0]}.", f"G0 Z{f3(z + 5)}", f"G1 Z{f3(z)} F{feed}")
        x = -30
        for i, y in enumerate(ys):
            if i: self.add(f"G1 Y{y}.")
            x = 150 if x == -30 else -30
            self.add(f"G1 X{x}.")
        self.add("G0 Z50.")

    def save(self, fn):
        self.add("M30", "%")
        open(fn, "w").write("\n".join(self.l) + "\n")
        return len(self.l)


# ---------------- OP10 ----------------
o = NC("O1010", "SYN-BRK-0101 OP10 BOTTOM A + PROFILE", 2.5)
o.tool("FACE", 1, "FACE MILL D50 5F", 3800, -30, 15)
o.face(0.0, 1900)
o.end_tool()
o.tool("ROUGH", 2, "END MILL D10 3F CARBIDE", 9500, -20, 40)
p = start_at(ring(PART.buffer(5.2, quad_segs=8), clockwise=True), (-5.2, 40))
for z in (-8.5, -17.0):
    o.path(p, z, 1400, (-20, 40))
o.add("G0 Z50.")
o.add("(OPERATION FINISH)")
p = start_at(ring(PART.buffer(5.0, quad_segs=8), clockwise=True), (-5.0, 40))
o.path(p, -17.0, 1000, (-20, 40))
o.end_tool()
o.tool("CHAMFER", 7, "CHAMFER MILL D6 90DEG", 10000, -20, 40)
p = start_at(ring(PART.buffer(1.0, quad_segs=8), clockwise=True), (-1.0, 40))
o.path(p, -1.5, 1000, (-20, 40))
o.end_tool()
n10 = o.save("OP10.nc")

# ---------------- OP20 ----------------
o = NC("O1020", "SYN-BRK-0101 OP20 TOP + POCKET + HOLES", 22.5)
o.tool("FACE", 1, "FACE MILL D50 5F", 3800, -30, 15)
o.face(20.3, 1900)
o.end_tool()

# 포켓 황삭: 벽·바닥 0.2 남김, 경사 진입, 안쪽에서 바깥쪽으로 반시계(하향 절삭)
o.tool("ROUGH", 2, "END MILL D10 3F CARBIDE", 9500, 47.2, 40, h_z=50)
o.add("G0 Z25.", "G1 Z20.5 F1400")
loops = [(47.2, 72.8, 37.2, 42.8), (41.2, 78.8, 31.2, 48.8), (35.2, 84.8, 25.2, 54.8)]
for z in (17.25, 14.2):
    o.add("G1 X47.2 Y40.", f"G1 X72.8 Z{f3(z)}")
    for x1, x2, y1, y2 in loops:
        o.add(f"G1 X{f3(x1)} Y{f3(y1)}", f"G1 X{f3(x2)}", f"G1 Y{f3(y2)}", f"G1 X{f3(x1)}", f"G1 Y{f3(y1)}")
    o.add("G1 X60. Y40.")
o.add("G0 Z50.")
o.end_tool()

o.tool("FACE", 1, "FACE MILL D50 5F", 3800, -30, 15)
o.face(20.0, 1200)
o.end_tool()
o.add("(STOCK TOP Z20.0)")

# 남은 외곽(Z17~20 플랜지) 정삭
o.tool("FINISH", 2, "END MILL D10 3F CARBIDE", 9500, -20, 40, h_z=50)
p = start_at(ring(PART.buffer(5.0, quad_segs=8), clockwise=True), (-5.0, 40))
for z in (18.5, 16.8):
    o.path(p, z, 1000, (-20, 40))
o.end_tool()

# 포켓 정삭: 바닥 지그재그 Z14 → 벽 한 바퀴(반시계)
o.tool("FINISH", 3, "END MILL D8 3F CARBIDE", 12000, 34.5, 40, h_z=50)
floor = POCKET.buffer(-4.2, quad_segs=16)
o.add("G0 Z25.", "G1 Z14.5 F1200", "G1 X40. Z14.0")
y, rows, flip = 24.2, [], False
while y < 55.8 + 1e-6:
    seg = floor.intersection(LineString([(0, y), (120, y)]))
    if not seg.is_empty:
        (xa, _), (xb, _) = list(seg.coords)[0], list(seg.coords)[-1]
        xa, xb = min(xa, xb), max(xa, xb)
        rows.append((y, xb, xa) if flip else (y, xa, xb)); flip = not flip
    y = round(y + 4.5, 3) if y + 4.5 < 55.8 else (55.8 if y < 55.8 else 99)
for yy, xs, xe in rows:
    o.add(f"G1 X{f3(xs)} Y{f3(yy)}", f"G1 X{f3(xe)}")
wall = start_at(ring(POCKET.buffer(-4.0, quad_segs=16), clockwise=False), (60, 24))
o.add("G1 X60. Y30.")
for x, yy in wall:
    o.add(f"G1 X{f3(x)} Y{f3(yy)}")
o.add("G1 X60. Y30.", "G0 Z50.")
o.end_tool()

# 센터 드릴(구멍 위 모서리 모따기 겸함): ⌀8 → 지름 9, M6 → 지름 7
o.tool("DRILL", 4, "SPOT DRILL D10 90DEG", 4000, 15, 12, h_z=25)
o.add("G98 G81 X15. Y12. Z15.5 R21. F400", "X105. Y12.", "X105. Y68.", "X15. Y68.", "X60. Y72. Z16.5", "X60. Y8.", "G80")
o.end_tool()
o.tool("DRILL", 5, "DRILL D7.8 CARBIDE", 4900, 15, 12, h_z=25)
o.add("G98 G83 X15. Y12. Z-3. R21. Q5. F730", "X105. Y12.", "X105. Y68.", "X15. Y68.", "G80")
o.end_tool()
o.tool("REAM", 6, "REAMER D8.020 SPECIAL", 2400, 15, 12, h_z=25)
o.add("G98 G85 X15. Y12. Z-1. R21. F720", "X105. Y12.", "X105. Y68.", "X15. Y68.", "G80")
o.end_tool()
o.tool("DRILL", 8, "DRILL D5.0 TAP DRILL", 6000, 60, 8, h_z=25)
o.add("G98 G83 X60. Y8. Z5. R21. Q5. F720", "X60. Y72.", "G80")
o.end_tool()
o.tool("TAP", 9, "TAP M6X1.0 OVERSIZE RIGID", 1500, 60, 8, h_z=25)
o.add("G98 G84 X60. Y8. Z8. R25. F1500", "X60. Y72.", "G80")
o.end_tool()

# 위쪽 모서리 C0.5: 바깥 외곽, 포켓 윗 모서리
o.tool("CHAMFER", 7, "CHAMFER MILL D6 90DEG", 10000, -20, 40, h_z=50)
p = start_at(ring(PART.buffer(1.0, quad_segs=8), clockwise=True), (-1.0, 40))
o.path(p, 18.5, 1000, (-20, 40))
o.add("G0 Z50.")
pk = start_at(ring(POCKET.buffer(-1.0, quad_segs=16), clockwise=False), (60, 26))
o.add("G0 X60. Y30.", "G0 Z23.", "G1 Z18.5 F1000")
for x, yy in pk:
    o.add(f"G1 X{f3(x)} Y{f3(yy)}")
o.add("G1 X60. Y30.")
o.end_tool()

# ⌀8 구멍 아래(A면 쪽) 모서리 C0.5: 백 모따기 공구, 구멍 중심으로 내려가 반지름 1.0 원호
o.tool("CHAMFER", 10, "BACK CHAMFER CUTTER HEAD D7.0 45DEG", 6000, 15, 12, h_z=25)
for x, yy in HOLES8:
    o.add(f"G0 X{x}. Y{yy}.", "G0 Z21.", "G1 Z-1.2 F1000", f"G1 X{f3(x + 1.0)} F300", f"G3 X{f3(x + 1.0)} Y{yy}. I-1. J0.", f"G1 X{x}.", "G1 Z21. F1000", "G0 Z25.")
o.end_tool()
n20 = o.save("OP20.nc")
print("OP10", n10, "blocks / OP20", n20, "blocks")
