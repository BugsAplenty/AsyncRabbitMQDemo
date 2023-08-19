import asyncio
import aio_pika
import base64
import cv2
import numpy as np

async def on_message(message: aio_pika.IncomingMessage):
    img_data = base64.b64decode(message.body)
    np_arr = np.frombuffer(img_data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.imwrite('received_image.jpg', image_np)
    # Acknowledge the message
    await message.ack()

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        # Creating channel
        channel = await connection.channel()
        # Declare a queue
        queue = await channel.declare_queue('image_queue', durable=True)
        # Start listening for messages from the queue
        await queue.consume(on_message)
        # This will keep the coroutine running and consuming indefinitely.
        await asyncio.Future()  


if __name__ == "__main__":
    asyncio.run(main())
