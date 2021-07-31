from ecommerce.local_settings import KAVENEGAR_API_KEY
from kavenegar import KavenegarAPI, APIException, HTTPException


def send_verify_code(receptor, message):
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            'sender': '10004346',
            'receptor': receptor,
            'message': message
        }
        response = api.sms_send(params)
        return response
    except APIException as e:
        print(str(e))
    except HTTPException as e:
        print(str(e))



