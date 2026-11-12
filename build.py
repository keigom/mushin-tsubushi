"""src.html から index.html を作る。

画面に出す文字だけを拾って Google Fonts の text= に渡し、
フォントの取り寄せを数十KBに抑える。

    python3 build.py
"""
import pathlib
import re
import urllib.parse

here = pathlib.Path(__file__).parent
src = (here / "src.html").read_text(encoding="utf-8")

# 画面に出ない文字（コメント、メタ情報、読み上げ用ラベル、デバッグ出力）は数えない
shown = re.sub(r"<!--.*?-->", "", src, flags=re.S)
shown = re.sub(r"/\*.*?\*/", "", shown, flags=re.S)
shown = re.sub(r"(?m)(^|[\s;{}])//[^\n]*", r"\1", shown)
shown = re.sub(r"<meta[^>]*>", "", shown)
shown = re.sub(r'aria-label="[^"]*"', "", shown)
shown = re.sub(r"console\.debug\([^)]*\)", "", shown)
shown = re.sub(r"setAttribute\('aria-label'[^\n]*", "", shown)

glyphs = sorted({ch for ch in shown if ord(ch) >= 0x3000} | set("0123456789, "))
text = urllib.parse.quote("".join(glyphs), safe="")

assert src.count("__GLYPHS__") == 1, "差し込み先が1か所ではありません"
out = src.replace("__GLYPHS__", text)

(here / "index.html").write_text(out, encoding="utf-8")
print(f"{len(glyphs)} 文字: {''.join(glyphs)}")
print(f"index.html {len(out.encode('utf-8')) / 1024:.1f} KB / フォントURLの長さ {len(text)}")
