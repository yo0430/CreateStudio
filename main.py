import asyncio
import argparse
import sys
import logging
from pathlib import Path

# WindowsコンソールでのUTF-8出力対応
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.pipeline.orchestrator import ContentPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("CreateStudio")

async def run_cli(args):
    pipeline = ContentPipeline()
    use_mock = not args.live or args.mock

    print("=" * 60)
    print("🎬 CreateStudio - 自律型マルチエージェント コンテンツ生成スタジオ")
    print("=" * 60)
    print(f"📌 テーマ: {args.topic}")
    print(f"⏱️ 目標秒数: {args.duration}秒")
    print(f"⚙️ 実行モード: {'モック（オフライン検証）' if use_mock else '実機（Ollama & MiniMax API）'}")
    print("=" * 60)

    try:
        result = await pipeline.run(
            topic=args.topic,
            duration_sec=args.duration,
            target_platform=args.platform,
            use_mock=use_mock
        )

        print("\n" + "=" * 60)
        print("🎉 パイプライン実行完了！")
        print("=" * 60)
        print(result.summary_report)
        print("\n📦 SNS投稿パッケージ:")
        print(f"   タイトル: {result.publication_package.video_title}")
        print(f"   ハッシュタグ: {' '.join(result.publication_package.tags)}")
        print(f"   動画ファイル: {result.master_video_path}")
        print("=" * 60)

    except Exception as e:
        logger.error(f"パイプライン実行中にエラーが発生しました: {e}", exc_info=True)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="CreateStudio 自律型動画コンテンツ生成CLI")
    parser.add_argument("--topic", "-t", type=str, default="AIが拓く未来都市の日常", help="動画の企画テーマ・トピック")
    parser.add_argument("--duration", "-d", type=float, default=15.0, help="目標動画再生秒数（秒）")
    parser.add_argument("--platform", "-p", type=str, default="youtube_shorts", help="対象プラットフォーム")
    parser.add_argument("--live", action="store_true", help="実機OllamaおよびMiniMax APIで実行")
    parser.add_argument("--mock", action="store_true", help="モックモードで高速テスト実行")
    args = parser.parse_args()

    asyncio.run(run_cli(args))

if __name__ == "__main__":
    main()
