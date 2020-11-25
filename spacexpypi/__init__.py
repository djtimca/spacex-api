"""Simple PyPi Wrapper for the SpaceX APIs."""

import logging
import aiohttp
import json

_LOGGER = logging.getLogger("spacex-pypi")

BASE_URL = "https://api.spacexdata.com/v4/"

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
        
        if response is not None:
            try:
                return json.loads(response)
            except json.decoder.JSONDecodeError as error:
                raise ValueError("Error decoding SpaceX Data (%s).", error)
            except Exception as error:
                raise ValueError("Unknown error in SpaceX data (%s),", error)
        else:
            raise ConnectionError("Error getting roadster data.")

    async def get_next_launch(self):
        """Get the next SpaceX Launch details."""
        response = {}

        launchURL = BASE_URL + "launches/next"

        async with await self._session.get(launchURL) as resp:
            response = await resp.text()

        if response is not None:
            try:
                formatted = json.loads(response)
                
                formatted["launch_site"] = await self.get_launchpad(formatted["launchpad"])
                formatted["rocket"] = await self.get_rocket(formatted["rocket"])
                formatted["cores_detail"] = await self.get_cores(formatted["cores"])
                formatted["payloads_detail"] = await self.get_payloads(formatted["payloads"])

                return formatted
            except json.decoder.JSONDecodeError as error:
                raise ValueError("Error decoding SpaceX Data (%s).", error)
            except Exception as error:
                raise ValueError("Unknown error in SpaceX data (%s),", error)
        else:
            raise ConnectionError("Error getting next launch data.")

    async def get_latest_launch(self):
        """Get the latest SpaceX Launch details."""
        response = {}

        launchURL = BASE_URL + "launches/latest"

        async with await self._session.get(launchURL) as resp:
            response = await resp.text()

        if response is not None:
            try:
                formatted = json.loads(response)
                
                formatted["launch_site"] = await self.get_launchpad(formatted["launchpad"])
                formatted["rocket"] = await self.get_rocket(formatted["rocket"])
                formatted["cores_detail"] = await self.get_cores(formatted["cores"])
                formatted["payloads_detail"] = await self.get_payloads(formatted["payloads"])

                return formatted
            except json.decoder.JSONDecodeError as error:
                raise ValueError("Error decoding SpaceX Data (%s).", error)
            except Exception as error:
                raise ValueError("Unknown error in SpaceX data (%s),", error)
        else:
            raise ConnectionError("Error getting latest launch data.")

    async def get_upcoming_launches(self):
        """Get all upcoming launches."""
        response = {}

        launchURL = BASE_URL + "launches/upcoming"

        async with await self._session.get(launchURL) as resp:
            response = await resp.text()

        if response is not None:
            try:
                return json.loads(response)
            except json.decoder.JSONDecodeError as error:
                raise ValueError("Error decoding SpaceX Data (%s).", error)
            except Exception as error:
                raise ValueError("Unknown error in SpaceX data (%s),", error)
        else:
            raise ConnectionError("Error getting upcoming launch data.")
    
    async def get_launchpad(self, launchpad_id:str):
        """Get the launchpad detail."""
        
        launchpadURL = BASE_URL + "launchpads/" + launchpad_id

        async with await self._session.get(launchpadURL) as resp:
            pad_details = await resp.json()

        return pad_details

    async def get_rocket(self, rocket_id:str):
        """Get the rocket detail."""

        rocketURL = BASE_URL + "rockets/" + rocket_id

        async with await self._session.get(rocketURL) as resp:
            rocket_details = await resp.json()

        return rocket_details

    async def get_cores(self, cores:list):
        """Get the core details."""

        coreURL = BASE_URL + "cores/"
        landpadURL = BASE_URL + "landpads/"

        cores_detail = []

        for this_core in cores:
            core_details = None
            landpad_details = None

            if this_core.get("core"):
                async with await self._session.get(coreURL + this_core["core"]) as resp:
                    core_details = await resp.json()

            if this_core.get("landpad"):
                async with await self._session.get(landpadURL + this_core["landpad"]) as resp:
                    landpad_details = await resp.json()

            this_core["details"] = core_details
            this_core["landpad"] = landpad_details

            cores_detail.append(this_core)

        return cores_detail

    async def get_payloads(self, payloads:list):
        """Get the payload details."""

        payloadURL = BASE_URL + "payloads/"

        payloads_detail = []

        for this_payload in payloads:
            async with await self._session.get(payloadURL + this_payload) as resp:
                payload_details = await resp.json()

            payloads_detail.append(payload_details)

        return payloads_detail