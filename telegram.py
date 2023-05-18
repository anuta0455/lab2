import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='6245040227:AAE0Cc2N33Bq3gaxDFG5a-Gcp-pMsIa6-eU')
dp = Dispatcher(bot)

questions = [
    {
        'question': 'В каком году Омский Авангард выиграл кубок Гагарина КХЛ?',
        'options': ['2021', '2015', '2011', '2023'],
        'answer': '1',
        'image': 'https://avatars.dzeninfra.ru/get-zen_doc/4032365/pub_608fc02fb8f34b04d25dbc8f_608fc175fe106d5922fc28ae/scale_1200',
        'welcome_image': 'https://cdn.cadelta.ru/media/covers/4/id4664/cover.jpg'
    },
    {
        'question': 'Как называлась произвольная программа, за которую Камила Валиева получила золото на Олимпиаде 2022?',
        'options': ['Китри', 'Анна Каренина', 'Круэлла', 'Болеро'],
        'answer': '4',
        'image': 'https://cdnn1.img.sputniknews.com/img/07e6/02/07/1092812415_0:33:3523:2015_1920x0_80_0_0_3f4856dab8a6d5bf57c5525a23a0389c.jpg'
    },
    {
        'question': 'Какой футболист принёс победу сборной Росии по футболу в матче против Испании на ЧМ-2018?',
        'options': ['Фёдор Смолов', 'Игорь Акинфеев', 'Марио Фернандес', 'Артём Дзюба'],
        'answer': '2',
        'image':'https://cdn.iz.ru/sites/default/files/styles/2048x1365/public/photo_item-2018-07/1530467133_2.JPG?itok=WS0E5gRR'
    },
    {
        'question': 'Как звали балерину, которая являлась фавориткой Николая II?',
        'options': ['Галина Уланова', 'Матильда Ксешинская', 'Майя Плисецкая', 'Анна Павлова'],
        'answer': '2',
        'image' :'https://mtdata.ru/u16/photo1A1E/20455901882-0/original.jpeg'
    },
    {
        'question': 'Гитаристом какой группы был Юрий Каспарян?',
        'options': ['Король и Шут', 'Сектор Газа', 'КИНО', 'Гражданская Оборона'],
        'answer': '3',
        'image' :'https://sun9-69.userapi.com/impg/k_EKBydWlrLKgQKic3E6QGU0KbZYa4LiXAakqQ/-2-BixJtYyU.jpg?size=1280x790&quality=95&sign=84acb8d853ed6017d7b0b0a93cb6af79&c_uniq_tag=Bgz0zTyXBCfs6YIynjIbXSk2KESSD2N9dm_gRr-pidc&type=album'
    }

]
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {
        'score': 0,
        'question_number': 0,
        'questions_asked': []
    }
    await ask_question(user_id)

async def ask_question(user_id):
    user_question_data = user_data[user_id]
    question_number = user_question_data['question_number']
    if question_number >= len(questions):
        await bot.send_message(user_id, f'Вы ответили на все вопросы! Ваш счет: {user_question_data["score"]}')
        await bot.send_photo(user_id, photo='https://i.ytimg.com/vi/a2wxKWKHLO4/maxresdefault.jpg')
        return
    question = questions[question_number]
    options = '\n'.join([f'{i+1}. {option}' for i, option in enumerate(question['options'])])
    await bot.send_message(user_id, f'{question["question"]}\n\n{options}')
    user_question_data['question_number'] += 1

@dp.message_handler()
async def answer_question(message: types.Message):
    user_id = message.from_user.id
    user_question_data = user_data[user_id]
    question_number = user_question_data['question_number'] - 1
    if question_number < 0 or question_number >= len(questions):
        return
    question = questions[question_number]
    answer = question['answer']
    if message.text == answer:
        user_question_data['score'] += 100
        await bot.send_message(user_id, 'Правильно! Вы заработали 100 очков.')
        question_image_url = question['image']
        await bot.send_photo(user_id, question_image_url)
    else:
        await bot.send_message(user_id, f'Неправильно. Правильный ответ: {answer}.')
    await ask_question(user_id)


if __name__ == '__main__':
    user_data = {}
    executor.start_polling(dp, skip_updates=True)