from dependency_injector.wiring import inject, Provide
from access_service.infrastructure.message_broker.kafka import KafkaMessageBroker
from access_service.application.common.gateway.verification_token import VerificationTokenGateway
from access_service.bootstrap.config import AccessServiceConfig
from access_service.domain.entities.verification_token import VerificationToken
from access_service.application.dto.verification_token import VerificationTokenDTO


async def init_message_broker(
    message_broker: KafkaMessageBroker 
):
    await message_broker.start()


@inject
async def consume_sms_results_in_background(
    message_broker: KafkaMessageBroker,
    config: AccessServiceConfig,
    verification_token_gateway: VerificationTokenGateway 
):
    async for msg in message_broker.start_consuming(topic=config.kafka.sms_result_topic):
        print(msg)
        verification_token_dto = VerificationTokenDTO(
            uid=msg["verification_token"]["metadata"]["uid"]["value"],
            expires_in=msg["verification_token"]["metadata"]["expires_in"]["value"],
            code=msg["verification_token"]["metadata"]["code"]["value"],
            token_id=msg["verification_token"]["token_id"]["value"]
        )
        await verification_token_gateway.save_verification_token(
            verification_token_dto=verification_token_dto
        )

    


async def close_message_broker(
    message_broker: KafkaMessageBroker
):
    await message_broker.stop()