# This source locate and provide the requested service

class service_locator():
    
    def __init__(self):
        self.list = [
            'login',
            'attraction',
            'relation',
            'location',
            'skeleton'
        ]

    def provide(self, service_name):
        
        if service_name == 'login':
            from services.login import login
            login = login.service()
            return login
        
        elif service_name == 'attraction':
            from services.attraction import attraction
            attraction = attraction.service()
            return attraction

        elif service_name == 'relation':
            from services.relation import relation
            relation = relation.service()
            return relation

        elif service_name == 'location':
            from services.location import location
            location = location.service()
            return location

        elif service_name == 'skeleton':
            from services.skeleton import skeleton
            skeleton = skeleton.service()
            return skeleton

        else:
            print('Not a valid service name')

    def list_services(self):
        print(self.list)
    