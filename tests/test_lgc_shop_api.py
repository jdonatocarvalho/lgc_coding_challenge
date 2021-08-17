import pytest
import json
from config import endpoints
from config.config import sample_methods
from utils.http_session import HttpSession
from utils.custom_asserters import assert_true, assert_equal
from utils.basic_logger import Logger
from utils.error_handling import *


class TestLgcShopAPI:

    @staticmethod
    @pytest.fixture
    def auth_tokens():
        Logger.info('Getting authentications tokens for LGC API...')
        response = HttpSession.send_request('post', endpoints.session_token('v1'))
        return {"access_token": "{}".format(response['accessToken']),
                "refresh_token": "{}".format(response['refreshToken'])}

    @staticmethod
    @pytest.mark.api
    @pytest.mark.sunny_day
    def test_1_validate_session_tokens(auth_tokens):
        Logger.debug('Validating LGC Shop API session tokens...')
        assert_true(auth_tokens['access_token'])
        Logger.info('Access Token is valid!')
        # Another way to handle errors and failures
        if auth_tokens['refresh_token']:
            Logger.info('Refresh Tokens is valid!')
        else:
            raise InvalidRefreshTokenException('There was a problem validating the Refresh Token')

    @staticmethod
    @pytest.mark.api
    @pytest.mark.sunny_day
    def test_2_validate_session_details(auth_tokens):
        Logger.debug('Validating LGC Shop API session details...')
        response = HttpSession.send_request('get', endpoints.session_details('v1', auth_tokens['access_token']))
        Logger.info('Session details returned successfully')
        assert_equal(response['refreshToken'], auth_tokens['refresh_token'])
        Logger.info('Session refresh token is valid!')

    @staticmethod
    @pytest.mark.api
    @pytest.mark.rainy_day
    def test_3_validate_required_token_for_shipping_countries_details():
        Logger.debug('Validating if a token is required to get shipping country details...')
        response = HttpSession.send_request('get', endpoints.shipping_country('v1'))
        response_body = json.loads(response.text)
        assert_equal(response.status_code, 401)
        assert_equal(response_body['errorMessage'], 'Invalid access token or the token has expired')
        Logger.info('Response message: {} - a valid token is required to get shipping country details'.format(
            response_body['errorMessage']))

    @staticmethod
    @pytest.mark.api
    @pytest.mark.sunny_day
    def test_4_validate_shipping_countries(auth_tokens):
        Logger.debug('Validating shipping countries list...')
        response = HttpSession.send_request('get', endpoints.shipping_country('v1'),
                                            auth_token=auth_tokens['access_token'])
        shipping_countries = len(response['items'])
        for item in response['items']:
            Logger.debug(item['name'])
        assert_equal(shipping_countries, 24)
        Logger.info('There are {} available countries for shipping!'.format(shipping_countries))

    @staticmethod
    @pytest.mark.api
    @pytest.mark.sunny_day
    def test_5_validate_products_details(auth_tokens, country):
        Logger.debug('Validating product details in: {}'.format(country))
        invalid_product_list = []
        Logger.debug("Fetching products details from the country - {}".format(country))
        response = HttpSession.send_request('get', endpoints.product_details('v2', country),
                                            auth_token=auth_tokens['access_token'])
        products_number = len(response['items'])
        Logger.info('There are {} available products in {}!'.format(products_number, country))
        assert_equal(products_number, 36)
        for item in response['items']:
            if item['sampleCollectionMethod'] not in sample_methods: invalid_product_list.append(item)
        if invalid_product_list:
            Logger.error('The following products do not respect the sample collection methods:')
            for product in invalid_product_list:
                Logger.error(product['title'] + " : " + product['sampleCollectionMethod'])
            pytest.fail()
        else:
            Logger.info('All products from {} respect the sample collection methods'.format(country))