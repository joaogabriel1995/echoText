from abc import ABC, abstractmethod


#   subscribe(
#     queue: string,
#     onMessage: (msg: Message, ack: () => void, nack: (requeue?: boolean) => void) => Promise<void>,
#     onError: (error: Error, msg: Message, ack: () => void, nack: (requeue?: boolean) => void) => Promise<void>
#   ): Promise<void>
#   ack(msg: Message): Promise<void>
#   nack(msg: Message, requeue: boolean): Promise<void>
class MessageBroker(ABC):

    @abstractmethod
    async def connection(self, url: str):
        pass

    @abstractmethod
    async def publish(self, queue: str, message: dict) -> None:
        pass

    @abstractmethod
    async def subscribe(self, queue: str, on_message) -> None:
        pass
