from spacex-pypi import SpaceX
import asyncio

async def main():
    api_client = SpaceX()

    success = await api_client.get_roadster_status()

    print(success)
    