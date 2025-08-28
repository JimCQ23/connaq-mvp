from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import dspy
from typing import Optional
from dotenv import load_dotenv
import os
from pydantic import field_validator
from app.data_types import Providers

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        
'''
load_dotenv(override=True)

class Environment(str, Enum):
    Production = "PROD"
    Development = "DEV"

class OpenAIConfig:
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    CONVERSATION_MODEL = "gpt-4o"
    EMBEDDING_MODEL = "text-embedding-3-small"


class AnthropicConfig:
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20240620"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ENVIRONMENT: Environment = Environment.Production
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
    APP_NAME: str = "CONNAQ"
    # QDRANT_URL: str = "http://localhost:6333"
    # QDRANT_API_KEY: Optional[str] = None
    DATABASE_URL: str = os.environ.get("DATABASE_URL")  # os.environ.get("DATABASE_URL")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    LLM_PROVIDER: str = Field(default="openai", env="LLM_PROVIDER")

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    def is_dev(self):
        return self.ENVIRONMENT == Environment.Development

    def is_prod(self):
        return self.ENVIRONMENT == Environment.Production

    @property
    def openai(self):
        return OpenAIConfig()

    @property
    def anthropic(self):
        return AnthropicConfig()


def get_4o_token_model():
    return dspy.OpenAI(
        model="gpt-4o", api_key=Settings().OPENAI_API_KEY, max_tokens=4096
    )


def initialize_dspy_with_configs(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    max_tokens: Optional[int] = None,
    set_global: bool = True,
):
    """
    This function initializes dspy with the given model, api_key, and max_tokens.
    It returns the model wrapper object in dspy.
    Args:
        model (str, optional): The model to use. Defaults to "gpt-4o".
        api_key (str, optional): The API key to use. Defaults to the OPENAI_API_KEY from the settings.
        max_tokens (int, optional): The maximum number of tokens to use. Defaults to 3000.
    Returns:
        dspy.OpenAI: The model wrapper object in dspy.
    """
    #dspy (short for DSPy) is an open-source framework by Stanford CRFM designed to 
    # build, train, and debug modular LLM (Large Language Model) applications 
    # — like agents, chains, and pipelines — using a PyTorch-style interface.
    
    if model is None:
        model = "gpt-4o"
    if api_key is None:
        api_key = Settings().OPENAI_API_KEY
    if max_tokens is None:
        max_tokens = 8192
    turbo = dspy.OpenAI(
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
    )
    # disable later , right now setting the model to the global level
    if set_global:
        dspy.settings.configure(lm=turbo)
    # this returns the model wrapper object in dspy
    return turbo

'''
def get_settings():
    return Settings()
