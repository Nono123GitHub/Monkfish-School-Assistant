from pyicloud import PyiCloudService
import time
import folium

# Login to iCloud
api = PyiCloudService('', '') #Noah: insert your icloud here

# Create a base map (centered at a default location initially)
mymap = folium.Map(location=[0, 0], zoom_start=15)

# List to store markers
markers = []

try:
    while True:
        time.sleep(1)  # Delay between location updates
        location_data = api.iphone.location()
        latitude = location_data['latitude']
        longitude = location_data['longitude']

        # Add marker for the current location if it is not already in the list
        if (latitude, longitude) not in markers:
            folium.Marker([latitude, longitude], popup=f"Lat: {latitude}, Lon: {longitude}").add_to(mymap)
            markers.append((latitude, longitude))

        # Save the updated map
        mymap.save("real_time_location.html")
except KeyboardInterrupt:
    print("Tracking stopped.")

# Save the final map
mymap.save("final_location_map.html")
