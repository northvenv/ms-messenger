

from access_service.domain.entities.verification_token import VerificationToken



def convert_verification_token_entity_to_dict(data: VerificationToken) -> dict:
    return {
        "token_id": str(data.token_id),
        "metadata": {
            "uid": str(data.metadata.uid),
            "expires_in": str(data.metadata.expires_in),
            "code": str(data.metadata.code)
        }
    }

def to_dict(self) -> dict:
    return {
        "token_id": str(self.token_id),
        "uid": str(self.metadata.uid),
        "expires_in": str(self.metadata.expires_in),
        "code": str(self.metadata.code)
    }