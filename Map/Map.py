# This Map application uses relation & attraction services

class Map():

    def __init__(self, attraction_service, relation_service):
        self.attraction_service = attraction_service
        self.relation_service = relation_service

    def test(self):
        self.attraction_service.test()
        self.relation_service.test()