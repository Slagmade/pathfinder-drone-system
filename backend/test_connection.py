from mavsdk import System
import asyncio

async def test():
    drone = System()
    await drone.connect()
    print("Connected to drone!")

asyncio.run(test())

