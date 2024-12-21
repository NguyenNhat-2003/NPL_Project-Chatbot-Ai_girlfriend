import asyncio
from rasa.core.agent import Agent
import os
os.chdir('../Dataset/')

class Rasa_Bot():

    def __init__(self, model_path='bot_1.tar.gz'):
        if not os.path.exists(model_path) or not os.path.isfile(model_path):
            print('Rasa: model not found')
        self.model_path = model_path
        self.agent = Agent.load(model_path)
        print('Rasa: Load model successfully')

    async def get_bot_response(self, user_input):
        responses = await self.agent.handle_text(user_input)
        if responses:
            return responses[0]['text']
        else:
            return "Em không hiểu ý anh"

    # Hàm chính để chạy bot
    def response(self, input):
        return asyncio.run(self.get_bot_response(input))

if __name__ == '__main__':
    bot = Rasa_Bot()

    print(bot.response("Em không rõ lắm"))
    print(bot.response("Em đi chơi không"))