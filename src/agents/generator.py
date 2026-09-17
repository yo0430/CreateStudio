import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import httpx
from src.core.config import settings
from src.core.models import CutPlan

logger = logging.getLogger(__name__)

class MiniMaxGenerator:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_concurrency: int = 2
    ):
        self.api_key = api_key or settings.MINIMAX_API_KEY
        self.base_url = (base_url or settings.MINIMAX_BASE_URL).rstrip("/")
        self.semaphore = asyncio.Semaphore(max_concurrency)

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    async def submit_t2v_task(self, cut: CutPlan) -> str:
        """MiniMax Video-01 APIにT2V生成タスクを送信し、task_idを取得する"""
        if not self.is_configured:
            raise ValueError("MINIMAX_API_KEY is not configured.")

        url = f"{self.base_url}/video_generation"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": cut.t2v_prompt,
            "model": "video-01",
            "prompt_optimizer": True
        }

        async with self.semaphore:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                task_id = data.get("task_id")
                if not task_id:
                    raise RuntimeError(f"Failed to obtain task_id from MiniMax API: {data}")
                logger.info(f"Submitted task for cut {cut.cut_id}: task_id={task_id}")
                return str(task_id)

    async def poll_task(
        self,
        task_id: str,
        initial_interval: float = 5.0,
        max_interval: float = 20.0,
        timeout: float = 300.0
    ) -> Dict[str, Any]:
        """指数バックオフでタスクの完了ステータスを監視する"""
        if not self.is_configured:
            raise ValueError("MINIMAX_API_KEY is not configured.")

        query_url = f"{self.base_url}/query/video_generation?task_id={task_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        start_time = asyncio.get_event_loop().time()
        current_interval = initial_interval

        async with httpx.AsyncClient(timeout=30.0) as client:
            while (asyncio.get_event_loop().time() - start_time) < timeout:
                response = await client.get(query_url, headers=headers)
                response.raise_for_status()
                data = response.json()

                status = data.get("status")
                logger.debug(f"Task {task_id} status: {status}")

                if status == "Success":
                    return data
                elif status == "Fail":
                    error_msg = data.get("base_resp", {}).get("status_msg", "Unknown generation error")
                    raise RuntimeError(f"MiniMax generation failed for task {task_id}: {error_msg}")

                await asyncio.sleep(current_interval)
                current_interval = min(current_interval * 1.3, max_interval)

        raise TimeoutError(f"Task {task_id} timed out after {timeout} seconds.")

    async def download_file(self, file_url: str, output_path: Path) -> Path:
        """生成された動画ファイルをストリーミングダウンロードする"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("GET", file_url) as response:
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
        logger.info(f"Downloaded clip to: {output_path}")
        return output_path

    async def generate_clip(
        self,
        cut: CutPlan,
        output_path: Optional[Path] = None,
        use_mock: bool = False
    ) -> Path:
        """カットの動画生成からダウンロードまでを一括実行する"""
        target_path = output_path or (settings.TEMP_DIR / "clips" / f"cut_{cut.cut_id}.mp4")

        if use_mock or not self.is_configured:
            return await self._generate_mock_clip(cut, target_path)

        task_id = await self.submit_t2v_task(cut)
        result = await self.poll_task(task_id)

        file_url = result.get("file_url") or result.get("download_url")
        if not file_url:
            raise RuntimeError(f"No download URL in task result: {result}")

        return await self.download_file(file_url, target_path)

    async def _generate_mock_clip(self, cut: CutPlan, output_path: Path) -> Path:
        """テスト・モック用の軽量ダミー動画ファイル生成"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # モック動画としてメタデータ付きヘッダーファイルを出力
        with open(output_path, "wb") as f:
            meta = f"Mock Video Clip for Cut {cut.cut_id}\nPrompt: {cut.t2v_prompt}\nDuration: {cut.duration_sec}s\n"
            f.write(meta.encode("utf-8"))
        logger.info(f"Generated mock clip: {output_path}")
        return output_path
