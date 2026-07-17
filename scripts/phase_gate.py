import argparse
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
DIST_FILE = ROOT_DIR / "dist" / "compiled_script.pine"
BUILD_SCRIPT = ROOT_DIR / "scripts" / "build.py"

REQUIRED_DIST_SNIPPETS = [
    "//@version=6",
    "indicator(",
    "zz_run()",
]


def has_utf8_bom(file_path: Path) -> bool:
    if not file_path.exists():
        return False
    return file_path.read_bytes().startswith(b"\xef\xbb\xbf")


def run_build(python_cmd: str) -> bool:
    result = subprocess.run(
        [python_cmd, str(BUILD_SCRIPT)],
        cwd=str(ROOT_DIR),
        check=False,
    )
    return result.returncode == 0


def verify_dist_content() -> list[str]:
    issues: list[str] = []

    if not DIST_FILE.exists():
        issues.append(f"distファイルが存在しません: {DIST_FILE}")
        return issues

    dist_text = DIST_FILE.read_text(encoding="utf-8")
    for required_snippet in REQUIRED_DIST_SNIPPETS:
        if required_snippet not in dist_text:
            issues.append(f"distに必須文字列がありません: {required_snippet}")

    return issues


def verify_bom() -> list[str]:
    issues: list[str] = []
    for file_path in [SRC_DIR / "main.pine", SRC_DIR / "zigzag.pine", DIST_FILE]:
        if not file_path.exists():
            issues.append(f"必須ファイルが見つかりません: {file_path}")
            continue
        if has_utf8_bom(file_path):
            issues.append(f"UTF-8 BOMが残っています: {file_path}")
    return issues


def print_manual_checklist() -> None:
    print("\n[MANUAL CHECKLIST] TradingView確認項目")
    print("1. 確定レッグと未確定点線が表示される")
    print("2. 水平線が確定ピボット起点で生成される")
    print("3. 足1終値突破だけでは遷移せず、足2終値の高安更新でのみ遷移する")
    print("4. Active→Flipped で色反転、Flipped→Broken で灰色ドット化する")
    print("5. BrokenがExpiry経過で削除され、短期足/長期足で描画破綻がない")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase7/8用のビルド同期・検証ゲート")
    parser.add_argument("--skip-build", action="store_true", help="build.py 実行を省略する")
    parser.add_argument("--python", default=sys.executable, help="build.py 実行に使うPythonコマンド")
    args = parser.parse_args()

    if not args.skip_build:
        print("[INFO] build.py を実行します")
        if not run_build(args.python):
            print("[FAIL] ビルドに失敗しました")
            return 1

    issues: list[str] = []
    issues.extend(verify_dist_content())
    issues.extend(verify_bom())

    if issues:
        print("[FAIL] Phase7/8 検証に失敗しました")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("[PASS] Phase7/8 検証に成功しました")
    print_manual_checklist()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
