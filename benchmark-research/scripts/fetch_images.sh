#!/usr/bin/env bash
# 벤치마크 리서치용 이미지 다운로더.
# 사용법: fetch_images.sh <output_dir> <url1> [url2 ...]
# - 파일을 01, 02 ... 순서로 저장하고, 확장자는 실제 파일 타입에서 추정한다.
# - HTTP 상태코드와 파일 타입을 출력하고, 실제 이미지가 아니거나 실패한 건은 삭제한다.
# 이렇게 검증까지 하는 이유: 깨진 링크나 HTML 에러 페이지가 이미지인 척 저장되는 일이 잦아서,
# 다운로드 직후 바로 걸러내야 리서치 문서에 쓸 수 있는 자료만 남는다.
#
# 권장 경로: bash <스킬경로>/scripts/fetch_images.sh docs/images "URL1" "URL2"

set -u

out_dir="${1:-}"
if [[ -z "$out_dir" ]]; then
  echo "usage: fetch_images.sh <output_dir> <url1> [url2 ...]" >&2
  exit 1
fi
shift
mkdir -p "$out_dir"

# 기존 파일과 충돌하지 않도록 현재 폴더의 마지막 번호 다음부터 이어서 저장한다.
last=$(ls "$out_dir" 2>/dev/null | grep -Eo '^[0-9]+' | sort -n | tail -1)
i=${last:-0}
ok=0
total=$#
for url in "$@"; do
  i=$((i + 1))
  idx=$(printf "%02d" "$i")
  tmp="$out_dir/.tmp_$idx"
  code=$(curl -s -L --max-time 60 -A "Mozilla/5.0" -w "%{http_code}" -o "$tmp" "$url")

  if [[ "$code" != "200" ]]; then
    echo "FAIL  $idx  http=$code  $url"
    rm -f "$tmp"
    continue
  fi

  # 실제 파일 타입으로 확장자 결정 (HTML 에러 페이지 등은 걸러낸다)
  mime=$(file -b --mime-type "$tmp")
  case "$mime" in
    image/jpeg) ext="jpg" ;;
    image/png)  ext="png" ;;
    image/gif)  ext="gif" ;;
    image/webp) ext="webp" ;;
    image/svg+xml) ext="svg" ;;
    *)
      echo "SKIP  $idx  not-an-image ($mime)  $url"
      rm -f "$tmp"
      continue
      ;;
  esac

  dest="$out_dir/$idx.$ext"
  mv "$tmp" "$dest"
  size=$(du -h "$dest" | cut -f1 | tr -d ' ')
  echo "OK    $idx  $mime  $size  -> $dest"
  ok=$((ok + 1))
done

echo "--- downloaded $ok/$total image(s) into $out_dir ---"
