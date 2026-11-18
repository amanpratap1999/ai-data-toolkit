"""
Lightweight Cloud Inference Client for ai-data-toolkit.
Optimized strictly for low-memory environments (8GB RAM).
Zero local weights, zero PyTorch overhead.
Supports: NVIDIA NIM (default), Groq, OpenRouter, and OpenAI.
"""

import os
import json
import time
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load .env from toolkit root if present
toolkit_root = Path(__file__).resolve().parent.parent
env_path = toolkit_root / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()


class CloudAIClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        # Prefer NVIDIA NIM by default, fallback to OpenAI format
        self.api_key = (
            api_key
            or os.getenv("NVIDIA_API_KEY")
            or os.getenv("OPENAI_API_KEY")
        )
        self.base_url = (
            base_url
            or os.getenv("NVIDIA_BASE_URL")
            or os.getenv("OPENAI_BASE_URL", "https://integrate.api.nvidia.com/v1")
        ).rstrip("/")
        self.model = (
            model
            or os.getenv("AI_MODEL", "minimaxai/minimax-m3.1-flash")
        )

        if not self.api_key:
            raise ValueError(
                "No API key found!\n"
                "Please set NVIDIA_API_KEY in ai-data-toolkit/.env\n"
                "(Get 1,000 free inference credits at: https://build.nvidia.com)"
            )

    def complete(
        self,
        prompt: str,
        system_prompt: str = "You are an expert data parsing assistant. Output strictly valid JSON without conversational filler.",
        temperature: float = 0.1,
        max_tokens: int = 2048,
        as_json: bool = True,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> Any:
        """
        Sends an inference request to the cloud endpoint with automatic retry & backoff.
        Returns parsed Python dict/list if as_json is True, else raw string.
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()
                raw_text = data["choices"][0]["message"]["content"].strip()

                if not as_json:
                    return raw_text

                # Clean markdown code fences if model wrapped them
                if "```" in raw_text:
                    parts = raw_text.split("```")
                    for part in parts:
                        clean_part = part.strip()
                        if clean_part.startswith("json"):
                            clean_part = clean_part[4:].strip()
                        if clean_part.startswith("{") and clean_part.endswith("}"):
                            raw_text = clean_part
                            break
                    else:
                        if raw_text.startswith("```"):
                            lines = raw_text.splitlines()
                            if lines[0].startswith("```"):
                                lines = lines[1:]
                            if lines and lines[-1].startswith("```"):
                                lines = lines[:-1]
                            raw_text = "\n".join(lines).strip()

                return json.loads(raw_text)

            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                last_error = e
                if attempt < max_retries:
                    sleep_time = retry_delay * (2 ** (attempt - 1))
                    print(f"⚠️ Inference request attempt {attempt} failed ({e}). Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
                else:
                    break

        raise RuntimeError(f"Cloud Inference failed after {max_retries} attempts: {last_error}")
