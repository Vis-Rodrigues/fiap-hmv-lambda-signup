import boto3
import logging
from utils.utils import return_response, get_secret_hash, get_environ


def resend_confirmation_code(body):
    client = boto3.client('cognito-idp')

    try:
        response = client.resend_confirmation_code(
            ClientId=get_environ('client_id'),
            SecretHash=get_secret_hash(body['email']),
            Username=body['email']
        )

        logging.info(response)

        return return_response(201, 'Código de confirmação reenviado com sucesso.')

    except client.exceptions.UserNotFoundException as e:
        logging.error(str(e))
        return return_response(404, 'Usuário não existe.')

    except client.exceptions.InvalidParameterException as e:
        logging.error(str(e))
        return return_response(422, 'Usuário já estava validado.')

    except client.exceptions.LimitExceededException as e:
        logging.error(str(e))
        return return_response(422, 'Limite de email diario atingido.')

    except client.exceptions.CodeDeliveryFailureException as e:
        logging.error(str(e))
        return return_response(422, 'Erro ao enviar código de verificação.')

    except Exception as e:
        logging.error(str(e))
        return return_response(500, "Ocorreu um erro, por favor, tente novamente.")
