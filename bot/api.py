import requests
import json

BASE_URL = 'http://127.0.0.1:8000/quran_bot/v1'

class CreateUser:
    def __init__(self, name, username, user_id, created_dt) -> None:
        self.name = name
        self.username = username
        self.user_id = user_id
        self.created_dt = created_dt
        
    def get_user(self):
        url = f"{BASE_URL}/bot-users"
        
        response = requests.get(url=url).text
        data = json.loads(response)
        user_eixst = any(i['user_id'] == str(self.user_id) for i in data)
        
        if not user_eixst:
            post = requests.post(url=url, data={
                'name': self.name,
                'username': self.username,
                'user_id': self.user_id,
                'created_dt': str(self.created_dt)
            })
            return "Foydalanuvchi yaratildi"
        
        return "Foydalanuchi mavjud"
    
    
# create = CreateUser("Eshmat", "Eshmat user", "87654321", "122:33:4:0")
