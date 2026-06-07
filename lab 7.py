import websockets
import asyncio

class WebSocketClient:
    def __init__(self):
       self.connection = None

    async def connect(self, url):
        try:
            self.connection = await websockets.connect(url, ping_interval=20, ping_timeout=20)
            print(f"З'єднання з {url} успішно встановлено")
        except ConnectionRefusedError:
            print("Помилка: Сервер відмовив у з'єднанні.")

    async def send_message(self, message):
        if self.connection:
            try:
                await self.connection.send(message)
                print(f"Відправлено: {message}")
            except Exception as e:
                print(f"Помилка при відправці повідомлення: {e}")
            else:
                print("Помилка: Немає активного з'єднання. Підключіться до сервера перед відправкою.")

    async def receive_message(self):
        if self.connection:
            try:
                message = await self.connection.recv()
                print(f"Отримано: {message}")
                return message
            except Exception as e:
                print(f"Помилка при отриманні повідомлення: {e}")
        else:
            print("Помилка: Немає активного з'єднання для отримання даних.")
            return None

    async def close_connection(self):
        if self.connection:
            await self.connection.close()
            print("З'єднання успішно закрито.")
        else:
            print("З'єднання вже закрито або не було встановлено.")

async def main():
    test_url = "wss://ws.postman-echo.com/raw"
    client = WebSocketClient()
    await client.connect(test_url)
    await client.send_message("Привіт! Це тестове повідомлення.")
    await client.receive_message()
    await client.send_message("відправка повідомлення серверу?")
    await client.receive_message()

    print("\n--- Тестування обробки помилок ---")
    await client.send_message("Це повідомлення не має відправитись.")

    await client.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
