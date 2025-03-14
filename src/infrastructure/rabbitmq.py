import aio_pika
import asyncio
from infrastructure.interfaces.message_broker import MessageBroker
import json


class RabbitMQ(MessageBroker):
    _instance = None
    _url = None
    _connection = None
    _is_connected = False
    _channel = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    @classmethod
    def set_url(cls, url: str):
        if cls._connection is None:
            cls._url = url
        else:
            raise RuntimeError(
                "A conexão já foi estabelecida. Não é possível alterar a URL."
            )

    async def connection(self):
        async with self._lock:
            if RabbitMQ._connection is None or RabbitMQ._connection.is_closed:
                try:
                    RabbitMQ._connection = await aio_pika.connect_robust(RabbitMQ._url)
                    RabbitMQ._is_connected = True
                except Exception as e:
                    print(f"Erro ao conectar ao RabbitMQ: {e}")
                    RabbitMQ._is_connected = False
                    raise

    async def get_channel(self):
        """Retorna sempre o mesmo canal, garantindo reutilização"""
        if RabbitMQ._connection is None or RabbitMQ._connection.is_closed:
            await self.connection()
        if RabbitMQ._channel is None or RabbitMQ._channel.is_closed:
            await self.create_channel()
        if RabbitMQ._channel is None:
            raise RuntimeError("Canal não foi inicializado corretamente.")
        return RabbitMQ._channel

    async def create_channel(self):
        """Cria o canal e levanta erro se falhar"""
        if RabbitMQ._connection is None:
            raise RuntimeError("Conexão não estabelecida antes de criar o canal.")
        try:
            RabbitMQ._channel = await RabbitMQ._connection.channel()
        except Exception as e:
            print(f"Erro ao criar canal no RabbitMQ: {e}")
            RabbitMQ._channel = None
            raise

    async def publish(self, queue: str, message: aio_pika.Message):
        try:
            channel = await self.get_channel()
            # Declara a fila
            # queue_obj = await channel.declare_queue(queue, durable=True)
            # Publica a mensagem serializada
            print(message)
            await channel.default_exchange.publish(message=message, routing_key=queue)
            print(f"Mensagem publicada na fila '{queue}': {message}")
        except Exception as e:
            print(f"Erro ao publicar mensagem no RabbitMQ: {e}")
            raise

    async def subscribe(self, queue: str, callback):
        """Escuta a fila e chama o callback para cada mensagem"""
        channel = await self.get_channel()

        if not channel:
            await self.connection()
        queue_obj = await channel.declare_queue(queue, durable=True)
        await queue_obj.consume(callback)
        print(f"Escutando a fila '{queue}'...")
