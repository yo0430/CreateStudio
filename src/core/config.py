import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "./output")).resolve()
    TEMP_DIR: Path = Path(os.getenv("TEMP_DIR", "./temp")).resolve()
    ASSETS_DIR: Path = (PROJECT_ROOT / "assets").resolve()

    MINIMAX_API_KEY: str = os.getenv("MINIMAX_API_KEY", "")
    MINIMAX_GROUP_ID: str = os.getenv("MINIMAX_GROUP_ID", "")
    MINIMAX_BASE_URL: str = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL_DIRECTOR: str = os.getenv("OLLAMA_MODEL_DIRECTOR", "llama3.1:8b")
    OLLAMA_MODEL_CRITIC: str = os.getenv("OLLAMA_MODEL_CRITIC", "llava:7b")

    FFMPEG_PATH: str = os.getenv("FFMPEG_PATH", "ffmpeg")

settings = Settings()
