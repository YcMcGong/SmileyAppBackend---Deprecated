# This file specifies the communication protocol for the DB service layer
import requests
DB_ENDPOINT = 'http://0.0.0.0:5000/get_user'
def test():
    response = requests.get(DB_ENDPOINT)
    data = response.json()
    return data

if __name__ == '__main__':
    response = requests.get(DB_ENDPOINT)
    #data = response.json()
    print(response)
    

'''
# Routing from here
@app.route('/', methods=['GET', 'POST'])
def testnull():
    return jsonify({'one':1, 'two':2})

if __name__ == '__main__':
    # app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
'''