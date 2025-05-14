import asyncio
from mavsdk import System

async def monitor_drone(port: int, label: str):
    """Connect to a drone and stream telemetry"""
    drone = System()
    
    print(f"[{label}] Connecting to UDP port {port}...")
    await drone.connect(system_address=f"udp://:{port}")
    
    # Wait for GPS fix and global position
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print(f"[{label}] GPS fix acquired")
            break
    
    # Continuous telemetry stream
    async for position in drone.telemetry.position():
        print(f"[{label}] Position: Lat {position.latitude_deg:.6f}°, "
              f"Lon {position.longitude_deg:.6f}°, "
              f"Alt {position.absolute_altitude_m:.1f}m")
    
    # Battery monitoring
    async for battery in drone.telemetry.battery():
        print(f"[{label}] Battery: {battery.remaining_percent*100:.1f}% remaining")

async def main():
    # Create tasks for both drones
    drone1 = monitor_drone(14550, "DRONE-1")
    drone2 = monitor_drone(14551, "DRONE-2")
    
    # Run concurrently
    await asyncio.gather(drone1, drone2)

if __name__ == "__main__":
    asyncio.run(main())
