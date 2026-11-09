"""Gera "../index.html" com todas as imagens de img/ embutidas em base64."""
import base64
import json
import pathlib

root = pathlib.Path(__file__).parent
template = (root / "index.html").read_text(encoding="utf-8")

marker = "const IMAGES = {};"
if marker not in template:
    raise SystemExit(f"Marcador '{marker}' não encontrado em index.html")

images = {
    p.stem: "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()
    for p in sorted((root / "img").glob("*.jpg"))
}

out = template.replace(marker, f"const IMAGES = {json.dumps(images)};")
target = root.parent / "index.html"
target.write_text(out, encoding="utf-8")
print(f"{target} gerado: {len(images)} imagens, {target.stat().st_size / 1e6:.1f} MB")
