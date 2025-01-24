import orjson
from access_service.application.dto.verification_token import VerificationTokenDTO



def convert_verification_token_dto_to_bytes(data: VerificationTokenDTO):
    return orjson.dumps(data)