import requests
import json

BASE_URL = 'http://127.0.0.1:8000/quran_bot/v1'

class AdminCommands:
    def __init__(self) -> None:
        pass

    def send_message_to_all_users(self):
        url = f"{BASE_URL}/bot-users"
        response = requests.get(url=url).text
        data = json.loads(response)
        all_user_ids = [i['user_id'] for i in data]
        return all_user_ids
                

        

            
    def users_info(self):
        url = f"{BASE_URL}/bot-users"
        response = requests.get(url=url).text
        data = json.loads(response)
        
        return data
        
        

# panel = AdminCommands()
# panel.users_info()
# print(panel.send_message_to_all_users("salom"))
    



