import asyncio
from mavsdk import System
from search_pattern import SearchPattern

async def connect_to_drone(port):
    """Connect to a drone using MAVSDK."""
    drone = System()
    await drone.connect(f"udp://127.0.0.1:{port}")
    
    print(f"Waiting for drone on port {port}...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone on port {port} connected!")
            break

    return drone

async def run_mission(drone, drone_id, center_lat, center_lon, width, height, spacing):
    """Setup and execute a search mission for a drone."""
    # Create search pattern
    search = SearchPattern(drone)
    
    # Upload mission
    await search.create_lawnmower(
        center_lat=center_lat, 
        center_lon=center_lon, 
        width=width, 
        height=height, 
        spacing=spacing
    )
    
    # Set return to launch after mission
    await drone.mission.set_return_to_launch_after_mission(True)
    
    # Wait for the drone to have a global position estimate
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print(f"Drone {drone_id}: Global position estimate OK")
            break
    
    # Execute mission
    await search.execute_mission()
    
    print(f"Drone {drone_id}: Mission started!")

async def main():
    """Main function to coordinate multiple drones."""
    # Connect to both drones
    drone1 = await connect_to_drone(14550)
    drone2 = await connect_to_drone(14551)
    
    # Default drone takeoff location
    default_lat = -35.363262
    default_lon = 149.165237
    
    # Define the overall search area
    search_width = 200  # meters
    search_height = 200  # meters
    lane_spacing = 30   # meters between passes
    
    # Divide area between drones
    drone_areas = await SearchPattern.divide_area(
        default_lat, default_lon, search_width, search_height, 2
    )
    
    # Create tasks for both drones
    tasks = []
    tasks.append(asyncio.create_task(
        run_mission(drone1, 1, drone_areas[0][0], drone_areas[0][1], 
                  drone_areas[0][2], drone_areas[0][3], lane_spacing)
    ))
    tasks.append(asyncio.create_task(
        run_mission(drone2, 2, drone_areas[1][0], drone_areas[1][1], 
                  drone_areas[1][2], drone_areas[1][3], lane_spacing)
    ))
    
    # Wait for both missions to complete
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
