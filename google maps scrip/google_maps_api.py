import googlemaps
import requests
import json

gmaps = googlemaps.Client(key="AIzaSyARWQ8zbkPU5X0xX7zZEAySW8OxQTQAyVc")
api_key = "AIzaSyARWQ8zbkPU5X0xX7zZEAySW8OxQTQAyVc"
def search_nearby_places():
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.displayName'
    }
    payload = {
        "includedTypes": ['point_of_interest'],
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": 15.2993,
                    "longitude": 74.1240
                },
                "radius": 1000
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.json())

# base_url = "https://maps.googleapis.com/maps/api/place/details/json"
# params = {
#     "fields": "name,rating,formatted_phone_number",
#     "place_id": "ChIJQbc2YxC6vzsRkkDzYv-H-Oo",
#     "key": "AIzaSyARWQ8zbkPU5X0xX7zZEAySW8OxQTQAyVc"
# }

# response = requests.get(base_url, params=params)
# print(response.json())

search_nearby_places()