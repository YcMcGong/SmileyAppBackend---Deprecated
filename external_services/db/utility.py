import uuid


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