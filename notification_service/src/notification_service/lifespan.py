import orjson
from dependency_injector.wiring import inject, Provide
from notification_service.message_broker.kafka import KafkaMessageBroker
from notification_service.bootstrap.di import KafkaContainer, ConfigContainer, SmsContainer
from notification_service.bootstrap.config import NotificationServiceConfig
from notification_service.dto.sms import Sms, SmsResult
from notification_service.sms_sender.sms import SmsSender


@inject
async def init_message_broker(
    message_broker: KafkaMessageBroker = Provide[KafkaContainer.message_broker]
):
    await message_broker.start()


@inject
async def consume_in_background(
    config: NotificationServiceConfig,
    message_broker: KafkaMessageBroker = Provide[KafkaContainer.message_broker],
    sms_sender: SmsSender = Provide[SmsContainer.sms_sender],
):
    async for msg in message_broker.start_consuming(topic=config.kafka.verification_token_topic):
        sms = Sms(
            number=msg["verification_token"]["metadata"]["phone_number"]['value'],
            text=str(msg["verification_token"]["metadata"]["code"]['value'])
        )
        print(sms)
        result_message = await sms_sender.send_sms(data=sms)
        result_bytes = orjson.dumps(
            SmsResult(
                sms_result=result_message,
                verification_token=msg["verification_token"]
            )
        )

        await message_broker.send_message(
            key=str(sms.number).encode(),  
            topic=config.kafka.sms_result_topic,  
            value=result_bytes,
        )


@inject
async def close_message_broker(
    message_broker: KafkaMessageBroker = Provide[KafkaContainer.message_broker]
):
    await message_broker.stop()
