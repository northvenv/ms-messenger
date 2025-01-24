from smsaero import SmsAero
from notification_service.sms_sender.base import BaseSmsSender
from notification_service.dto.sms import Sms
from notification_service.sms_sender.config import SmsConfig


def get_sms_api(config: SmsConfig) -> SmsAero:
    return SmsAero(
        email=config.email,
        api_key=config.api_key
    )


class SmsSender(BaseSmsSender):
    def __init__(
        self,
        sms_api: SmsAero
    ):
        self.sms_api: SmsAero = sms_api

    async def send_sms(self, data: Sms) -> dict:
        try:
            result = await self.sms_api.send_sms(
                number=data.number,
                text=data.text
            )
            return result
        finally:
            await self.sms_api.close_session()