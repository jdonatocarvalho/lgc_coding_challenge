import json
import requests
from utils.basic_logger import Logger


class HttpSession():

    @staticmethod
    # Json Body and param requests can also be send using this method
    def send_request(request_type, endpoint, body=None, params=None, auth_token=None):
        if auth_token:
            headers['Authorization'] = 'Bearer {}'.format(auth_token)
        try:
            response = getattr(requests, request_type)(endpoint, json=body, headers=headers, params=params)
            response.raise_for_status()
            Logger.debug('Received response: {} with the status code: {}'.format(json.loads(response.text),
                                                                                 response.status_code))
            return json.loads(response.text)
        except requests.exceptions.HTTPError as err:
            Logger.error('There was a problem regarding the request status code: {} with the response {}'.format(err,
                                                                                                                 json.loads(
                                                                                                                     response.text)))
            return response
        except requests.exceptions.RequestException as e:
            Logger.error('There was a problem sending the {} request due to exception: {}'.format(request_type, e))


headers = {
    'Host': 'shop-api.letsgetchecked.com',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept': '*/*',
    'Content-Type': 'application/json'
}