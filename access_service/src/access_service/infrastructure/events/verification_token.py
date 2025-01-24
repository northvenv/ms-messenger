from access_service.infrastructure.events.base import EventHandler
from access_service.domain.events.verification_token import VerificationTokenCreatedEvent
from access_service.infrastructure.events.converter import (
    convert_event_to_broker_message,
    convert_event_to_json
)


class VerificationTokenCreatedEventHandler(EventHandler[VerificationTokenCreatedEvent, None]):
    async def handle(self, event: VerificationTokenCreatedEvent):
        try:
            await self.message_broker.send_message(
                key=str(event.event_id).encode(),
                topic=self.broker_topic,
                value=convert_event_to_broker_message(event=event)
            )
        except Exception as exc:
            raise exc
