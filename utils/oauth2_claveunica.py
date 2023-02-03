from urllib.parse import urlencode

import uuid
import requests


# generate random UUIDv4 form state param
def generate_state():
    return str(uuid.uuid4())


# Generate redirect url to claveUnica
def join_url_with_params(url, params):
    return '{url}?{params}'.format(url=url, params=params)


# Obtain encoded parameters in url for request authorization_code ClaveUnica
def get_url_params_authorization_code(client_id, redirect_uri, state=uuid.uuid4()):
    return urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'scope': 'openid run name email',
        'redirect_uri': redirect_uri,
        'state': state,
    })


# Obtain encoded parameters in url for request ClaveUnica access_token
def get_params_access_token(client_id, client_secret, redirect_uri, code, state=uuid.uuid4()):
    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code': code,
        'state': state,
    }


#  headers for request authorization_code"""
def get_headers_authorization_code():
    return {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'User-Agent': 'My User Agent 1.0'
    }


#  headers for bearer oauth2 authentication
def get_headers_bearer_token(access_token):
    return {
        'Authorization': 'Bearer {access_token}'.format(access_token=access_token),
        'Accept': 'application/json',
        'User-Agent': 'My User Agent 1.0'
    }


# Build ClaveUnica Login Url
def get_url_login_claveunica(url, client_id, redirect_uri, state=uuid.uuid4()):
    return join_url_with_params(url, get_url_params_authorization_code(client_id, redirect_uri, state))


# POST request for authorization_code to Clave Unica
def request_authorization_code(url, client_id, client_secret, redirect_uri, code, state=uuid.uuid4()):
    resp = requests.post(url, data=get_params_access_token(
        client_id, client_secret, redirect_uri, code, state), headers=get_headers_authorization_code())
    if resp.status_code != 200:
        raise Exception('Clave Unica http status error: {status_code}. Error al obtener authorization_code de Clave Unica.'.format(
            status_code=resp.status_code))
    return resp.json()


#  POST Request to obtain information of Clave Unica user
def request_info_user(url, access_token):
    resp = requests.post(url, headers=get_headers_bearer_token(access_token))
    if resp.status_code != 200:
        raise Exception('Clave Unica http status error: {status_code}. Error al obtener infouser de Clave Unica.'.format(
            status_code=resp.status_code))
    return resp.json()
