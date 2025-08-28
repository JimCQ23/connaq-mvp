from enum import Enum
from typing import List

Embedding = List[float]


class VectorStores(Enum):
    FAISS = "faiss"
    QDRANT = "qdrant"
    COGNITIVE_SEARCH = "cognitive_search"
    LANCEDB = "lancedb"


class EmebeddingProviders(Enum):
    OPENAI = "openai"
    BEDROCK = "bedrock"
    MINILM = "minilm"
    COHERE = "cohere"
    GEMINI = "gemini"
    AZURE_OPENAI = "azure_openai"


class LLM_Providers(Enum):
    OPENAI_GPT_35 = "openai_gpt35"
    OPENAI_GPT_4 = "openai_gpt4"
    OPENAI_GPT_4_O = "openai_gpt4o"
    LLAMA_7B = "llama_7b"
    COHERE = "cohere"
    GEMINI = "gemini"


class Providers(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"
