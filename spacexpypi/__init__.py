"""Simple PyPi Wrapper for the SpaceX APIs."""

import logging
import aiohttp
import json

_LOGGER = logging.getLogger("spacex-pypi")

BASE_URL = "https://api.spacexdata.com/v3/"

class SpaceX:
    def __init__(self):
        """Initialize the session."""
        self.retry = 5
        self._session = aiohttp.ClientSession()

    async def close(self):
        """Close the session."""
        await self._session.close()

    async def get_roadster_status(self):
        """Get the roadster status."""
        response = {}

        roadsterURL = BASE_URL + "roadster"

        async with await self._session.get(roadsterURL) as resp:
            response = await resp.text()
        
        return json.loads(response)

    async def get_next_launch(self):
        """Get the next SpaceX Launch details."""
        response = {}

        launchURL = BASE_URL + "launches/next"

        async with await self._session.get(launchURL) as resp:
            response = await resp.text()

        return json.loads(response)

    async def get_upcoming_launches(self):
        """Get all upcoming launches."""
        response = {}

        launchURL = BASE_URL + "launches/upcoming"

        async with await self._session.get(launchURL) as resp:
            response = await resp.text()

        return json.loads(response)
