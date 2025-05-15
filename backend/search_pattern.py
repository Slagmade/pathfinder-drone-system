from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)
import asyncio

class SearchPattern:
    """Implements various search patterns for disaster response drones."""
    
    def __init__(self, drone):
        self.drone = drone
        
    async def create_lawnmower(self, center_lat, center_lon, width, height, spacing):
        """
        Creates a lawnmower pattern search centered at given coordinates.
        
        Args:
            center_lat: Center latitude in degrees
            center_lon: Center longitude in degrees
            width: Width of the search area in meters
            height: Height of the search area in meters
            spacing: Distance between passes in meters
        """
        mission_items = []
        altitude = 30  # meters
        speed = 5      # m/s
        
        # Convert width/height from meters to degrees (approximate)
        # 111,111 meters = 1 degree of latitude
        # 111,111 * cos(latitude) meters = 1 degree of longitude
        import math
        lat_degree_dist = 111111.0
        lon_degree_dist = 111111.0 * math.cos(math.radians(center_lat))
        
        width_deg = width / lon_degree_dist
        height_deg = height / lat_degree_dist
        spacing_deg = spacing / lat_degree_dist
        
        # Calculate corners of search area
        min_lat = center_lat - (height_deg / 2)
        max_lat = center_lat + (height_deg / 2)
        min_lon = center_lon - (width_deg / 2)
        max_lon = center_lon + (width_deg / 2)
        
        # Generate lawnmower waypoints
        current_lat = min_lat
        direction = 1  # 1 for east, -1 for west
        
        while current_lat <= max_lat:
            if direction == 1:
                # Add eastward point
                mission_items.append(MissionItem(
                    current_lat,
                    min_lon,
                    altitude,
                    speed,
                    True,  # is_fly_through
                    float('nan'),  # gimbal_pitch_deg
                    float('nan'),  # gimbal_yaw_deg
                    MissionItem.CameraAction.NONE,
                    float('nan'),  # loiter_time_s
                    float('nan'),  # camera_photo_interval_s
                    float('nan'),  # acceptance_radius_m
                    0,  # yaw_deg
                    float('nan')  # camera_photo_distance_m
                ))
                
                # Add eastward point
                mission_items.append(MissionItem(
                    current_lat,
                    max_lon,
                    altitude,
                    speed,
                    True,
                    float('nan'),
                    float('nan'),
                    MissionItem.CameraAction.NONE,
                    float('nan'),
                    float('nan'),
                    float('nan'),
                    0,
                    float('nan')
                ))
            else:
                # Add westward point
                mission_items.append(MissionItem(
                    current_lat,
                    max_lon,
                    altitude,
                    speed,
                    True,
                    float('nan'),
                    float('nan'),
                    MissionItem.CameraAction.NONE,
                    float('nan'),
                    float('nan'),
                    float('nan'),
                    0,
                    float('nan')
                ))
                
                # Add westward point
                mission_items.append(MissionItem(
                    current_lat,
                    min_lon,
                    altitude,
                    speed,
                    True,
                    float('nan'),
                    float('nan'),
                    MissionItem.CameraAction.NONE,
                    float('nan'),
                    float('nan'),
                    float('nan'),
                    0,
                    float('nan')
                ))
            
            # Move to next line
            current_lat += spacing_deg
            direction *= -1  # Change direction
        
        # Create and upload mission plan
        mission_plan = MissionPlan(mission_items)
        print(f"Uploading mission with {len(mission_items)} items...")
        
        await self.drone.mission.upload_mission(mission_plan)
        print("Mission uploaded!")
        
    async def execute_mission(self):
        """Arms drone and starts the mission."""
        print("Arming drone...")
        await self.drone.action.arm()
        
        print("Starting mission...")
        await self.drone.mission.start_mission()
        
    async def divide_area(center_lat, center_lon, width, height, num_drones):
        """
        Divides a search area among multiple drones.
        Returns list of (center_lat, center_lon, width, height) for each drone.
        """
        areas = []
        
        if num_drones == 2:
            # Split area horizontally into two equal parts
            areas.append((
                center_lat - (height/4)/111111.0,  # South half center
                center_lon,
                width,
                height/2
            ))
            
            areas.append((
                center_lat + (height/4)/111111.0,  # North half center
                center_lon,
                width,
                height/2
            ))
        
        return areas
