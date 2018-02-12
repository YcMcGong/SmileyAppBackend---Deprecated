# This source locate and provide the requested service

class service_locator():
    
    def __init__(self):
        self.list = [
            'login',
            'attraction'
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

        else:
            print('Not a valid service name')

    def list_services(self):
        print(self.list)
    