from config.config import api_url


def session_token(api_version):
    return f'{api_url}/{api_version}/session'


def session_details(api_version, access_token):
    return f'{api_url}/{api_version}/session/{access_token}'


def shipping_country(api_version):
    return f'{api_url}/{api_version}/shipping/country'


def product_details(api_version, country):
    return f'{api_url}/{api_version}/testkit/products/{country}'