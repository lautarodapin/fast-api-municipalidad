from httpx import AsyncClient

async def get_client():
    client = AsyncClient(timeout=60)
    try:
        yield client
    finally:
        await client.aclose()
        del client