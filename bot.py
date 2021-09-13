from chai_py import ChaiBot, Update
import npu
import json
import requests

BOT_NAME = "Rinna"
USR_NAME = "Person"

API_TOKEN = 'api_pqqqNkmGKXbDmIVgwoXLBAPmyiAouNTlKP'
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

class Bot(ChaiBot):
    def setup(self):
        self.logger.info("Starting setup...")
        self.chat_log = []
        npu.api('LsqV0Z2PP-_A_tceb_Mtkx16i1r1knOrxW3_Q0b-HD8', deployed=True)
        self.model_id = '60ca2a1e54f6ecb69867c72c'
        self.kwargs = {
            'response_length': 50,
            'remove_input': True,
            'do_sample': True,
            'top_p': 0.95,
            'temperature': 0.9
        }
        self.headers = {"Authorization": f"Bearer {API_TOKEN}"}
        self.context = f'{BOT_NAME} is 16 years old. {BOT_NAME} is a high school girl living in Tokyo, Japan. She loves to watch anime and read manga. She is cute and friendly. She has a crush on .\n'

    def query(self, payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    def get_message(self, text):
        quote_count = 0
        for i in range(len(text)):
            if text[i] == '"':
                quote_count += 1
                if quote_count % 2 == 1 and i+1 < len(text) and not text[i+1].isalpha() and not text[i+1].isnumeric():
                    break
        j = text.find(f'{USR_NAME} said:')
        if j == -1:
            j = len(text)
        return text[:min(i, j-1)]

    async def on_message(self, update: Update) -> str:
        user_reply = update.latest_message.text
        if user_reply == self.FIRST_MESSAGE_STRING:
            self.chat_log.append((BOT_NAME, f'Hellooo! :) <3 I\'m {BOT_NAME}.'))
            self.chat_log.append((USR_NAME, f'Hi! Nice to meet you.'))
            self.chat_log.append((BOT_NAME, f'Lovely to meet you too! <3 Tell me a little story about today?'))
            return f'Hellooo! :) <3 I\'m {BOT_NAME}, tell me a little story about today?'

        self.chat_log.append((USR_NAME, user_reply))
        history = '\n'.join([f'{sender} said: "{message}"' for (sender, message) in self.chat_log])
        # print(history)
        data = [self.context + history + f'\n{BOT_NAME} said: "']

        output = npu.predict(self.model_id, data, self.kwargs)
        text = output[0]['generated_text']

        response = self.get_message(text)
        self.chat_log.append((BOT_NAME, response))

        return response