from abc import ABC



class BaseSmsSender(ABC):
    async def send_sms(self, data: ...):
        raise NotImplementedError