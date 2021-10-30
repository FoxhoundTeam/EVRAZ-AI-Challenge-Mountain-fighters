from src.settings import CENTRIFUGO_API_KEY, CNETRIFUGO_HOST
import json
import requests



class Centrifugo:
    api_key = CENTRIFUGO_API_KEY

    def send_model(self, channel, instance, serializer, method='publish'):
        data = {
            'type': 'model',
            'model': instance.__class__.__name__,
            'data': serializer(instance).data
        }
        self.send(method, channel, data=data)


    def send(self, method, channel, data={}):
        command = {
            "method": method,
            "params": {
                "channel": channel,
                "data": data,
            }
        }
        data = json.dumps(command)
        headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + self.api_key}
        print(requests.post(f"{CNETRIFUGO_HOST}/api", data=data, headers=headers))
