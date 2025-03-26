from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings
from typing import Union, List

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str

    # CORS settings
    CORS_ORIGINS: list[str]


    @field_validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    def print_content(self):
        print("===PROJECT SETTINGS=============================================")
        for key, value in self.model_dump().items():
            # Mask sensitive information
            if "PASSWORD" in key or "SECRET" in key:
                print(f"\t{key}: ********")
            else:
                print(f"\t{key}: {value}")
        print("================================================================")
