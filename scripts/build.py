import os
import re

SRC_DIR = "src"
DIST_DIR = "dist"
ENTRY_POINT = "main.pine"
OUTPUT_FILE = "compiled_script.pine"

def resolve_includes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # '//#include "パス"' を正規表現で検出して置換
    pattern = r'//#include\s+"([^"]+)"'
    
    def replace_match(match):
        include_rel_path = match.group(1)
        # src ディレクトリからの相対パスとして解決
        include_path = os.path.join(SRC_DIR, include_rel_path)
        if os.path.exists(include_path):
            # 再帰的にネストしたincludeも解決できるようにする
            return resolve_includes(include_path)
        else:
            raise FileNotFoundError(f"エラー: 指定されたインクルードファイルが見つかりません: {include_path}")

    return re.sub(pattern, replace_match, content)

def build():
    os.makedirs(DIST_DIR, exist_ok=True)
    entry_path = os.path.join(SRC_DIR, ENTRY_POINT)
    
    try:
        bundled_code = resolve_includes(entry_path)
        out_path = os.path.join(DIST_DIR, OUTPUT_FILE)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(bundled_code)
        print(f"[SUCCESS] ビルド完了! 出力先: {out_path}")
    except Exception as e:
        print(f"[ERROR] ビルド失敗: {e}")

if __name__ == "__main__":
    build()
