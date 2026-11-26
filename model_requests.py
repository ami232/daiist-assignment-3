"""Bounded retries for read-only judge requests; never replay write-tool flows."""

import asyncio
import sys

from google.genai.errors import APIError
from langchain_google_genai.chat_models import GoogleAPIError


async def judge_request(operation):
    for attempt in range(4):
        try:
            return await operation()
        except (APIError, GoogleAPIError) as error:
            text = str(error).lower()
            transient = (
                "503" in text
                or "unavailable" in text
                or ("429" in text and ("per minute" in text or "perminute" in text))
            )
            if not transient or attempt == 3:
                raise
            print(
                f"Transient judge service error; retry {attempt + 1}/3.",
                file=sys.stderr,
                flush=True,
            )
            await asyncio.sleep(2 ** (attempt + 1))
