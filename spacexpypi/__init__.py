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

    def close(self):
        """Close the session."""
        await self._session.close()

    async def get_roadster_status(self):
        """Get the roadster status."""
        response = {}

        roadsterURL = BASE_URL + "roadster"

        async with await self._session.get(roadsterURL) as resp:
            response = await resp.text()
        
        return json.dumps(response)
