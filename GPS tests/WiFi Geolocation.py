import os
import math
from pywifi import PyWiFi, const, Profile

# Example access points with known locations (replace these with your actual known locations)
access_points = {
    "00:11:22:33:44:55": {"name": "AP1", "location": (37.7749, -122.4194)},  # San Francisco
    "66:77:88:99:AA:BB": {"name": "AP2", "location": (34.0522, -118.2437)},  # Los Angeles
    "CC:DD:EE:FF:00:11": {"name": "AP3", "location": (40.7128, -74.0060)}   # New York
}

# Function to scan Wi-Fi networks and extract relevant details using pywifi (Windows)
def scan_networks(interface='wlan0'):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first available Wi-Fi interface
    iface.scan()  # Start scanning
    result = iface.scan_results()  # Get scan results
    
    networks = []
    for network in result:
        network_info = {
            "SSID": network.ssid,
            "BSSID": network.bssid,
            "signal_strength": network.signal
        }
        networks.append(network_info)
    
    return networks

# Function to estimate the user's location based on nearby networks' signal strength
def estimate_location(networks):
    estimated_lat, estimated_lon = 0, 0
    total_weight = 0

    for network in networks:
        if network['BSSID'] in access_points:
            ap = access_points[network['BSSID']]
            rssi = network['signal_strength']
            
            # Assume the signal strength (RSSI) gives us an approximate distance using a basic model
            distance = 10 ** ((27.55 - (20 * math.log10(2400)) + abs(rssi)) / 20)  # Simplified formula

            # Use the distance to weight the known location (inverse square law)
            weight = 1 / (distance ** 2)
            total_weight += weight
            estimated_lat += ap['location'][0] * weight
            estimated_lon += ap['location'][1] * weight

    if total_weight > 0:
        estimated_lat /= total_weight
        estimated_lon /= total_weight

    return estimated_lat, estimated_lon

# Main function to scan networks and estimate the location
def main():
    print("Scanning for Wi-Fi networks...")
    networks = scan_networks()
    
    if not networks:
        print("No networks found.")
        return
    
    print("\nFound networks:")
    for net in networks:
        print(f"SSID: {net['SSID']}, BSSID: {net['BSSID']}, Signal Strength: {net['signal_strength']}")
    
    # Estimate the location based on signal strength
    estimated_location = estimate_location(networks)
    print(f"\nEstimated Location: Latitude = {estimated_location[0]}, Longitude = {estimated_location[1]}")

# Run the main function
if __name__ == "__main__":
    main()
