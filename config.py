"""
Configuration utilities for OpenAI and other services
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables with explicit path
load_dotenv(dotenv_path=".env.local")


class OpenAIConfig:
    """Configuration class for OpenAI API settings."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.embeddings_api_key = os.getenv("OPENAI_EMBEDDINGS_API_KEY", self.api_key)
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.embeddings_base_url = os.getenv(
            "OPENAI_EMBEDDINGS_BASE_URL", self.base_url
        )
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.embeddings_model = os.getenv(
            "OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small"
        )
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

    def get_chatgpt_config(self) -> Dict[str, Any]:
        """Get configuration for ChatOpenAI."""
        config = {"model": self.model_name, "temperature": self.temperature}

        if self.api_key:
            config["openai_api_key"] = self.api_key

        if self.base_url and self.base_url != "https://api.openai.com/v1":
            config["openai_api_base"] = self.base_url

        return config

    def get_embeddings_config(self) -> Dict[str, Any]:
        """Get configuration for OpenAI embeddings."""
        config = {"model": self.embeddings_model}

        if self.embeddings_api_key:
            config["openai_api_key"] = self.embeddings_api_key

        if (
            self.embeddings_base_url
            and self.embeddings_base_url != "https://api.openai.com/v1"
        ):
            config["openai_api_base"] = self.embeddings_base_url

        return config

    def is_configured(self) -> bool:
        """Check if OpenAI is properly configured."""
        return bool(self.api_key)

    def is_embeddings_configured(self) -> bool:
        """Check if OpenAI embeddings is properly configured."""
        return bool(self.embeddings_api_key)

    def validate_config(self) -> Optional[str]:
        """Validate configuration and return error message if invalid."""
        if not self.api_key:
            return "OPENAI_API_KEY is not set in environment variables"

        if not self.embeddings_api_key:
            return "OPENAI_EMBEDDINGS_API_KEY is not set in environment variables"

        if not self.base_url:
            return "OPENAI_BASE_URL is not set"

        if not self.embeddings_base_url:
            return "OPENAI_EMBEDDINGS_BASE_URL is not set"

        return None


def get_openai_config() -> OpenAIConfig:
    """Get OpenAI configuration instance."""
    return OpenAIConfig()


# Example usage configurations for common providers
COMMON_CONFIGS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "description": "Official OpenAI API",
    },
    "azure": {
        "base_url": "https://your-resource.openai.azure.com/openai/deployments/your-deployment",
        "description": "Azure OpenAI Service",
    },
    "local": {
        "base_url": "http://localhost:8000/v1",
        "description": "Local OpenAI-compatible server",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "description": "Ollama local server",
    },
    "vllm": {"base_url": "http://localhost:8000/v1", "description": "vLLM server"},
}

test_jd = """Responsibilities:
Coding and Development:
Writing clean, efficient, and reusable Python code, developing and maintaining web applications and backend services. 
Frameworks and Libraries:
Utilizing Python frameworks like Django, Flask, and others, as well as experience with libraries for data manipulation, web development, and machine learning. 
Software Design and Architecture:
Designing and implementing RESTful APIs, microservices, and scalable solutions, contributing to software architecture discussions. 
Testing and Debugging:
Developing and implementing automated tests, debugging applications, and ensuring code quality through code reviews"""
