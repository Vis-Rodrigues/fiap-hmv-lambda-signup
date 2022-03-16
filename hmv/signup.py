import boto3
import logging
from utils.utils import return_response, get_secret_hash, get_environ


def signup(body):
    client = boto3.client('cognito-idp')

    try:

        response = client.sign_up(
            ClientId=get_environ('client_id'),
            SecretHash=get_secret_hash(body['email']),
            Username=body['email'],
            Password=body['password'],
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': body['name']
                },
                {
                    'Name': 'email',
                    'Value': body['email']
                },
                {
                    'Name': 'phone_number',
                    'Value': body['phone_number']
                },
                {
                    'Name': 'custom:doc_type',
                    'Value': body['doc_type']
                },
                {
                    'Name': 'custom:document_number',
                    'Value': body['document_number']
                }
            ],
            ClientMetadata={
                'username': body['name']
            },
        )

        logging.info(response)

        return return_response(201, 'Conta criada com sucesso.')

    except client.exceptions.UsernameExistsException as e:
        logging.error(str(e))
        return return_response(422, 'Já existe uma conta com este mesmo email.')

    except client.exceptions.InvalidPasswordException as e:
        logging.error(str(e))
        return return_response(422, 'A senha não atende aos requisitos mínimos.')

    except client.exceptions.InvalidParameterException as e:
        logging.error(str(e))
        return return_response(422, 'Existem parâmetros inválidos.')

    except client.exceptions.CodeDeliveryFailureException as e:
        logging.error(str(e))
        return return_response(422, 'Erro ao enviar código de verificação.')

    except client.exceptions.LimitExceededException as e:
        logging.error(str(e))
        return return_response(422, 'Limite de email diario atingido.')

    except Exception as e:
        logging.error(str(e))
        return return_response(500, "Ocorreu um erro, por favor, tente novamente.")
