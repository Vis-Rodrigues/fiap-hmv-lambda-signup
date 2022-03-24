import boto3
import requests
import logging
import json
from utils.utils import return_response, get_secret_hash, get_environ, logger_info, logger_error


def signup(body):
    client = boto3.client('cognito-idp')

    try:

        response = client.sign_up(
            ClientId=get_environ('client_id'),
            SecretHash=get_secret_hash(body['email']),
            Username=body['email'],
            Password=body['senha'],
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': body['nome']
                },
                {
                    'Name': 'email',
                    'Value': body['email']
                },
                {
                    'Name': 'phone_number',
                    'Value': body['telefone']
                },
                {
                    'Name': 'custom:doc_type',
                    'Value': body['docTipo']
                },
                {
                    'Name': 'custom:document_number',
                    'Value': body['docNumero']
                }
            ],
            ClientMetadata={
                'username': body['nome']
            },
        )

        logger_info(response)
        response_api = post_user(body)

        return return_response(201, 'Conta criada com sucesso.', response_api)

    except client.exceptions.UsernameExistsException as e:
        logger_error(str(e))
        return return_response(422, 'Já existe uma conta com este mesmo email.')

    except client.exceptions.InvalidPasswordException as e:
        logger_error(str(e))
        return return_response(422, 'A senha não atende aos requisitos mínimos.')

    except client.exceptions.InvalidParameterException as e:
        logger_error(str(e))
        return return_response(422, 'Existem parâmetros inválidos.')

    except client.exceptions.CodeDeliveryFailureException as e:
        logger_error(str(e))
        return return_response(422, 'Erro ao enviar código de verificação.')

    except client.exceptions.LimitExceededException as e:
        logger_error(str(e))
        return return_response(422, 'Limite de email diario atingido.')

    except Exception as e:
        logging.error(str(e))
        return return_response(500, "Ocorreu um erro, por favor, tente novamente.")


def post_user(body):
    headers = {'Content-Type': 'application/json'}
    try:
        logger_info('Iniciando o cadastro do usuário por API.')
        response_api = requests.post('{}/usuarios'.format(get_environ('url_user')),
                                     headers=headers, data=json.dumps(body))

        response_body = response_api.json()
        logger_info('Response: {}, Status Code: {}'.format(response_body, response_api.status_code))

        response_api.raise_for_status()

        return response_body

    except requests.exceptions.HTTPError as error:
        logger_error(error)
        return return_response(500, "Ocorreu um erro ao cadastrar usuário no banco de dados, por favor, tente novamente.")