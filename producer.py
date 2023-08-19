import asyncio
import aio_pika
import base64

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=base64.b64encode(open('image.png', 'rb').read())),
            routing_key='image_queue'
        )

if __name__ == "__main__":
    asyncio.run(main())
