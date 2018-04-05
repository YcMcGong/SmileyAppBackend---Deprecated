# This Map application uses relation & attraction services

class Map():

    def __init__(self, attraction_service, relation_service):
        self.attraction_service = attraction_service
        self.relation_service = relation_service

    def test(self):
        self.attraction_service.test()
        self.relation_service.test()

    def get_map_attractions(self, user_id, rule = 'default'):
        # return a list of user_id's
        friends = self.relation_service.show_all_friends(user_id)
        # insert self
        friends.insert(0, user_id)

        # return a dict which contains:
        #   {
        #   isSuccess: Boolean, 
        #   errMessage: String, 
        #   attractions: {attraction_ID1: [date_time, location],
        #     attraction_ID2: [date_time, location], ..., }
        #   }
        attractions = self.attraction_service.attraction_list_get(friends)
        if (rule == 'default'):
            # remove duplicate entries
            attractions = list(set(attractions))

    def gps_to_place_list(self, lat, lng):
        pass

if __name__ == "__main__":
    custom_data = {
        'isSuccess': True,
        'errMessage': "",
        'attractions': {'attraction_ID1': ['2018-03-30-23:59:59', 'a1'], 
                        'attraction_ID2': ['2018-04-01-00:00:01', 'a2']}
        }
    test_isSuccess = custom_data['isSuccess']
    test_errMessage = custom_data['errMessage']
    test_attractions_list = custom_data['attractions']
    print(test_isSuccess)
    print(test_errMessage)
    print(test_attractions_list)
