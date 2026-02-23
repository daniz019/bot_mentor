import os
from mem0 import MemoryClient

_client = None


def get_client() -> MemoryClient:
    global _client
    if _client is None:
        _client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))
    return _client


def add(user_id: int, user_message: str, assistant_reply: str):
    get_client().add(
        [{"role": "user", "content": user_message}, {"role": "assistant", "content": assistant_reply}],
        user_id=str(user_id),
    )


def get_all(user_id: int) -> list[str]:
    response = get_client().get_all(filters={"AND": [{"user_id": str(user_id)}]})
    results = response.get("results", []) if isinstance(response, dict) else response
    return [item.get("memory") or item.get("content", "") for item in results if item.get("memory") or item.get("content")]
