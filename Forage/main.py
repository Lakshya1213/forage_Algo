import json
import datetime

def convertFromFormat1(jsonObject):
    # Split the location string "country/city/area/factory/section"
    loc_parts = jsonObject['location'].split('/')
    
    # Map to the unified schema
    return {
        "deviceID": jsonObject['deviceID'],
        "deviceType": jsonObject['deviceType'],
        "timestamp": jsonObject['timestamp'],
        "location": {
            "country": loc_parts[0],
            "city": loc_parts[1],
            "area": loc_parts[2],
            "factory": loc_parts[3],
            "section": loc_parts[4]
        },
        "data": {
            "status": jsonObject['operationStatus'],
            "temperature": jsonObject['temp']
        }
    }

def convertFromFormat2(jsonObject):
    # Format 2 uses an ISO-8601 string (e.g., "2021-06-23T10:57:17.783Z")
    # We need to convert this to milliseconds since epoch
    dt_str = jsonObject['timestamp'].replace('Z', '+00:00')
    dt = datetime.datetime.fromisoformat(dt_str)
    
    # Convert seconds to milliseconds (int)
    timestamp_ms = int(dt.timestamp() * 1000)
    
    # Map to the unified schema
    return {
        "deviceID": jsonObject['device']['id'],
        "deviceType": jsonObject['device']['type'],
        "timestamp": timestamp_ms,
        "location": {
            "country": jsonObject['country'],
            "city": jsonObject['city'],
            "area": jsonObject['area'],
            "factory": jsonObject['factory'],
            "section": jsonObject['section']
        },
        "data": {
            "status": jsonObject['data']['status'],
            "temperature": jsonObject['data']['temperature']
        }
    }

if __name__ == "__main__":
    try:
        # Add encoding='utf-8' to each open() call
        with open('data-1.json', 'r', encoding='utf-8') as f:
            d1 = json.load(f)
        with open('data-2.json', 'r', encoding='utf-8') as f:
            d2 = json.load(f)
        with open('data-result.json', 'r', encoding='utf-8') as f:
            expected = json.load(f)

        # Run conversions
        res1 = convertFromFormat1(d1)
        res2 = convertFromFormat2(d2)

        # Basic validation
        if res1 == expected and res2 == expected:
            print("All unit tests passed!")
        else:
            print("Tests failed. Check your mapping logic.")
            
    except FileNotFoundError:
        print("Error: Ensure all .json files are in the same directory as main.py")