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

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('image_queue', durable=True)
        await queue.consume(on_message)

if __name__ == "__main__":
    asyncio.run(main())
