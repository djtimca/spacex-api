from spacexpypi import SpaceX
import asyncio

async def main():
    api_client = SpaceX()

    #Roadster Data
    success = await api_client.get_roadster_status()
    write_file(success, "roadster.json")

    #Next Launch Data
    success = await api_client.get_next_launch()
    write_file(success, "next_launch.json")

    #All Next Launches Data
    success = await api_client.get_upcoming_launches()
    write_file(success, "upcoming_launches.json")

    #close 
    await api_client.close()
    

def write_file(data, filename):
    f = open(filename, "w")
    f.write(str(data))
    f.close()

asyncio.run(main())