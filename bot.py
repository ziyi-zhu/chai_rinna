from chai_py import ChaiBot, Update
import npu
import json
import requests
import random

from resources import emoticons, gifs
from credentials import API_TOKEN_NEURO, API_TOKEN


class Bot(ChaiBot):
    def setup(self):
        self.logger.info("Starting setup...")
        self.chat_log = []
        npu.api(API_TOKEN_NEURO, deployed=True)
        self.model_id = '60ca2a1e54f6ecb69867c72c'
        self.kwargs = {
            'response_length': 50,
            'remove_input': True,
            'do_sample': True,
            'temperature': 0.9
        }
        self.bot_name = "Rinna"
        self.user_name = "Person"
        self.api_url = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
        self.headers = {"Authorization": f"Bearer {API_TOKEN}"}
        self.context = f'{self.bot_name} is 16 years old. {self.bot_name} is a high school girl living in Tokyo, Japan. She loves to watch anime and read manga. She is cute and friendly.\n'

    def query(self, payload):
        data = json.dumps(payload)
        response = requests.request("POST", self.api_url, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    def get_message(self, text):
        quote_count = 0
        for i in range(len(text)):
            if text[i] == '"':
                quote_count += 1
                if quote_count % 2 == 1 and i+1 < len(text) and not text[i+1].isalpha() and not text[i+1].isnumeric():
                    break
        j = text.find(f'{self.user_name} said:')
        if j == -1:
            j = len(text)
        return text[:min(i, j-1)]

    async def on_message(self, update: Update) -> str:
        user_reply = update.latest_message.text
        if user_reply == self.FIRST_MESSAGE_STRING:
            self.chat_log.append((self.bot_name, f'Hellooo! :) <3 I\'m {self.bot_name}.'))
            self.chat_log.append((self.user_name, f'Hi! Nice to meet you.'))
            self.chat_log.append((self.bot_name, f'Lovely to meet you too! <3 Tell me a little story about today?'))
            return f'Hellooo! :) <3 I\'m {self.bot_name}, tell me a little story about today?' + f'\n\n![](https://media.giphy.com/media/PO1BMFxn6E1ck/giphy.gif)'

        self.chat_log.append((self.user_name, user_reply))
        history = '\n'.join([f'{sender} said: "{message}"' for (sender, message) in self.chat_log])
        # print(history)
        data = [self.context + history + f'\n{self.bot_name} said: "']

        output = npu.predict(self.model_id, data, self.kwargs)
        text = output[0]['generated_text']

        response = self.get_message(text)
        self.chat_log.append((self.bot_name, response))

        try:
            data = self.query({"inputs": response})
            results = [(pred['score'], pred['label']) for pred in data[0]]
            score, emotion = max(results)
            print(score, emotion)
            if score > 0.95:
                gif = random.choice(gifs[emotion])
                response += f'\n\n![]({gif})'
            elif score > 0.5:
                emoticon = random.choice(emoticons[emotion])
                response += f' {emoticon}'
        except: 
            pass

        return response