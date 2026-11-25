"""Bounded retries for transient provider failures; no retry on daily quota."""
import asyncio


def transient_error(error):
    detail = str(error).lower()
    if any(term in detail for term in ("requests per day", "generaterequestsperday", "perday")):
        return False
    return isinstance(error, (TimeoutError, ConnectionError)) or any(term in detail for term in (
        "429", "500", "502", "503", "504", "resource_exhausted", "deadline_exceeded",
        "high demand", "cannot connect", "connection reset", "timed out"))


async def invoke_with_recovery(operation, events, stage, attempts=3):
    for attempt in range(attempts):
        try:
            return await operation()
        except Exception as error:
            retry = transient_error(error) and attempt + 1 < attempts
            events.append({"stage": stage, "attempt": attempt + 1,
                           "error_type": type(error).__name__, "retry": retry})
            if not retry:
                raise
            await asyncio.sleep(5 * (attempt + 1))
