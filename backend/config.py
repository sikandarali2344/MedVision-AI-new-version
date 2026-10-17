from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
ROOT = Path(__file__).resolve().parents[1]
class Settings(BaseSettings):
    secret_key: str = "development-only-change-me"
    access_token_expire_minutes: int = 720
    database_url: str = "sqlite:///./medvision.db"
    model_path: str = "artifacts/best_densenet121_baseline.pth"
    class_names: str = "COVID19,NORMAL,PNEUMONIA,TB"
    max_upload_mb: int = 10
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)
    @property
    def classes(self): return [x.strip() for x in self.class_names.split(",") if x.strip()]
    @property
    def resolved_model_path(self):
        p = Path(self.model_path)
        return p if p.is_absolute() else ROOT / p
@lru_cache
def get_settings(): return Settings()
settings = get_settings()
