from googleplaces import GooglePlaces

""" Image Resize """

API_KEY = 'AIzaSyBWI6d4t99Hpdxv8DSUXBoPwn1m10QxCCc'

def gps_to_place_list(Lat, Lng):
    # Set up google places API
    google_places = GooglePlaces(API_KEY)
    # Search for place
    query_result = google_places.nearby_search(lat_lng = {'lat': Lat, 'lng': Lng}, radius = 100,
    type = 'point_of_interest')

    # If found result within radius
    data = []
    if query_result.places:
        
        for place in query_result.places:
            
            name = place.name
            format_lat = float(place.geo_location['lat'])
            format_lng = float(place.geo_location['lng'])
            # place.get_details()
            # address = place.formatted_address
            data.append({'name': name, 'lat': format_lat, 'lng': format_lng})

    return data