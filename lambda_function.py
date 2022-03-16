import logging
from hmv.signup import signup
from hmv.confirm_signup import confirm_sign_up
from hmv.resend_code import resend_confirmation_code
from utils.utils import get_body, return_response


def lambda_handler(event, context):
    route = get_route(event)
    body = get_body(event['body'])

    if route == '/fiap-hmv/v1/signup':
        return signup(body)
    elif route == '/fiap-hmv/v1/signup/confirm':
        return confirm_sign_up(body)
    elif route == '/fiap-hmv/v1/signup/resend-code':
        return resend_confirmation_code(body)


def get_route(event):
    resource: str = event.get('resource', None)
    if not resource:
        logging.error('The resource key was not found in event.')
        raise BaseException()

    logging.info('Resource: {}'.format(resource))

    return resource
