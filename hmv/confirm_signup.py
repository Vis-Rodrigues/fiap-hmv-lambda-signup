import boto3
from utils.utils import return_response, get_secret_hash, get_environ, logger_info, logger_error


def confirm_sign_up(body):
    client = boto3.client('cognito-idp')

    try:
        response = client.confirm_sign_up(
            ClientId=get_environ('client_id'),
            SecretHash=get_secret_hash(body['email']),
            Username=body['email'],
            ConfirmationCode=body['code'],
        )

        logger_info(response)

        return return_response(201, 'Usuário validado com sucesso.', response)

    except client.exceptions.UserNotFoundException as e:
        logger_error(str(e))
        return return_response(404, 'Usuário inexistente.')

    except client.exceptions.ExpiredCodeException as e:
        logger_error(str(e))
        return return_response(422, 'Código de validação expirado.')

    except client.exceptions.NotAuthorizedException as e:
        logger_error(str(e))
        return return_response(422, 'Usuário já estava validado.')

    except client.exceptions.CodeMismatchException as e:
        logger_error(str(e))
        return return_response(422, 'Código de validação inválido.')

    except Exception as e:
        logger_error(str(e))
        return return_response(500, "Ocorreu um erro, por favor, tente novamente.")
