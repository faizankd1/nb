from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    ollama_base_url: str = "http://127.0.0.1:11434"
    generation_model: str = "gemma2:2b"
    embedding_model: str = "nomic-embed-text"

    # All durable application data lives below data/ by default.
    data_path: Path = ROOT / "data"
    uploads_path: Path | None = None
    extracted_path: Path | None = None
    chroma_path: Path | None = None
    metadata_path: Path | None = None
    logs_path: Path | None = None
    jobs_path: Path | None = None
    sqlite_path: Path | None = None

    collection_name: str = "document_chunks"
    chunk_size: int = 1800
    chunk_overlap: int = 300
    top_k: int = 4
    retrieval_candidate_multiplier: int = 8
    hybrid_lexical_weight: float = 0.20
    lexical_candidate_limit: int = 20
    embedding_batch_size: int = 16
    min_similarity: float = 0.25
    max_file_mb: int = 100
    max_batch_mb: int = 500
    max_upload_files: int = 50
    ingestion_workers: int = 1
    inference_concurrency: int = 1
    admin_username: str = "admin"
    admin_password: str = ""
    temperature: float = 0.0
    timeout: int = 90
    tesseract_cmd: str = ""
    ocr_enabled: bool = True
    max_pdf_pages: int = 5000
    max_image_pixels: int = 40_000_000
    extraction_block_rows: int = 1000
    max_question_parts: int = 6
    max_context_chars: int = 9000
    verify_answers: bool = True
    recovery_on_startup: bool = True

    # Resolve configuration relative to the application, not whichever folder
    # happened to be current when Uvicorn was started.  This makes the launcher
    # scripts, tests, and manual starts behave consistently.
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    def model_post_init(self, __context):
        configured_data_path = Path(self.data_path).expanduser()
        # Keep a relative DATA_PATH relative to the application directory,
        # rather than to an arbitrary terminal working directory.
        self.data_path = (configured_data_path if configured_data_path.is_absolute()
                          else ROOT / configured_data_path).resolve()
        defaults = {
            "uploads_path": self.data_path / "uploads",
            "extracted_path": self.data_path / "extracted",
            "chroma_path": self.data_path / "chroma_db",
            "metadata_path": self.data_path / "metadata",
            "logs_path": self.data_path / "logs",
            "jobs_path": self.data_path / "jobs",
            "sqlite_path": self.data_path / "metadata" / "documents.sqlite3",
        }
        for key, default in defaults.items():
            value = getattr(self, key)
            setattr(self, key, Path(value).expanduser().resolve() if value else default.resolve())

settings = Settings()
