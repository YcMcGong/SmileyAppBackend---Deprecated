import uuid
import googlemaps

def generate_unique_ID():
    return str(uuid.uuid1())

def compute_partition_key(lat, lng):
    return str(int(float(lat) * 1000 + int(float(lng))))

def generate_partition_key_list(lat, lng):
    return [
        str(int(float(lat) + 1) * 1000 + int(float(lng) + 1)),
        str(int(float(lat) - 1) * 1000 + int(float(lng) + 1)),
        str(int(float(lat)) * 1000 + int(float(lng) + 1)),
        str(int(float(lat) + 1) * 1000 + int(float(lng) - 1)),
        str(int(float(lat) - 1) * 1000 + int(float(lng) - 1)),
        str(int(float(lat)) * 1000 + int(float(lng) - 1)),
        str(int(float(lat) + 1) * 1000 + int(float(lng))),
        str(int(float(lat) - 1) * 1000 + int(float(lng))),
        str(int(float(lat)) * 1000 + int(float(lng)))
    ]

def gps_to_address(lat, lng):

    gmaps = googlemaps.Client(key='AIzaSyBWI6d4t99Hpdxv8DSUXBoPwn1m10QxCCc')
    data = gmaps.reverse_geocode((lat, lng))
    address = data[0]['formatted_address']
    
    return address