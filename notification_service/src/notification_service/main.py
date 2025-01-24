import asyncio
from notification_service.lifespan import (
    init_message_broker,
    consume_in_background,
    close_message_broker
)
from notification_service.bootstrap.di import setup_containers


async def main():
    config = setup_containers()
    await init_message_broker()

    consume_task = asyncio.create_task(consume_in_background(config.config()))

    try:
        await consume_task
    except KeyboardInterrupt:
        pass
    finally:
        consume_task.cancel()
        await close_message_broker()


if __name__ == "__main__":
    asyncio.run(main())
