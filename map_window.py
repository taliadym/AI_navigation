import tkinter
import tkintermapview
import requests

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Map View Example")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# Define the API key and the base URL for GraphHopper
API_KEY = "fed000dd-1a51-4e9f-99e3-7d545148fac7"  # Replace with your GraphHopper API key
BASE_URL = "https://graphhopper.com/api/1/route"

# Define the start and end positions for routing
start_position = (31.77684535183484, 35.20548894735849)  # The Knesset
end_position = (31.77106032261776, 35.215891967541204)  # Beit Hanassi


def marker_click(marker):
    print(f"Marker clicked - text: {marker.text}  position: {marker.position}")


# Set initial position and add markers
map_widget.set_position(*start_position, marker=False)
# map_widget.set_zoom(17)
marker_2 = map_widget.set_marker(*start_position, text="The Knesset", command=marker_click)
marker_3 = map_widget.set_marker(*end_position, text="Beit Hanassi", command=marker_click)
# set a path
path_1 = map_widget.set_path([marker_2.position, marker_3.position])


# Set parameters for the API request
params = {
    "point": [f"{start_position[0]},{start_position[1]}", f"{end_position[0]},{end_position[1]}"],
    "profile": "car",  # Use the profile suitable for the mode of transport (e.g., car, bike, foot)
    "locale": "en",
    "instructions": "true",  # To get detailed instructions and list of roads
    "calc_points": "true",
    "key": API_KEY
}

# Make the request to GraphHopper API
response = requests.get(BASE_URL, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Extract road instructions from the response
    if "paths" in data and len(data["paths"]) > 0:
        instructions = data["paths"][0]["instructions"]
        print("List of roads and instructions:")
        for instruction in instructions:
            street_name = instruction.get("street_name", "Unknown Road")
            distance = instruction.get("distance", 0)
            time = instruction.get("time", 0)
            print(f"Road: {street_name}, Distance: {distance:.2f} meters, Time: {time / 1000:.2f} seconds")
    else:
        print("No paths found in the response.")
else:
    print(f"Error: {response.status_code}, {response.text}")



# # Function to fetch and draw route
# def fetch_and_draw_route(start, end):
#     # Build the request URL for GraphHopper
#     params = {
#         "point": [f"{start[0]},{start[1]}", f"{end[0]},{end[1]}"],
#         "vehicle": "car",  # Choose vehicle type, e.g., car, bike, foot
#         "locale": "en",
#         "instructions": "false",
#         "key": API_KEY,
#     }
#
#     # Make the request to GraphHopper
#     try:
#         response = requests.get(BASE_URL, params=params)
#         response.raise_for_status()
#         data = response.json()
#         print(data)  # Output route data for debugging
#
#         # Extract the route points
#         if "paths" in data and len(data["paths"]) > 0:
#             points = data["paths"][0]["points"]["coordinates"]
#             path_coords = [(lat, lon) for lon, lat in points]  # Reverse order to (lat, lon)
#
#             # Draw the route path on the map
#             map_widget.set_path(path_coords, color="blue", width=2)
#             print("Route drawn on the map.")
#         else:
#             print("No route found.")
#     except Exception as e:
#         print(f"Error fetching route: {e}")
#
#
# # Fetch and draw the route when the application starts
# fetch_and_draw_route(start_position, end_position)

# Start the tkinter main loop
root_tk.mainloop()
