from httpx import AsyncClient
def get_client():
    client = AsyncClient(timeout=60)
    try:
        yield client
    finally:
        client.aclose()
        del client