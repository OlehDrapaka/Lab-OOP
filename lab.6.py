import requests
class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        if response.status_code == 200:
            print("Помилок не виявлено")
            return response.json()
        else:
            print("Помилка:", response.status_code)

    def post(self, endpoint, data):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)

        if response.status_code == 201:
            print("Створено пост:", response.json())
        else:
            print("Помилка:", response.status_code)

client = RestClient("https://jsonplaceholder.typicode.com")
print(client.get("posts"))
data = {
    "title": "Мій новий пост",
    "body": "Це текст",
    "userId": 1
}

data2 = {
    "title": "Попередній пост",
    "body": "Це текст",
    "userId": 2
}

client.post("posts", data)
client.post("posts", data2)

