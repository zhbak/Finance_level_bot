from telebot import types
from database import database
from bot_structure import variables, buttons

async def text_question_answer(chat_id: int):
    index = await database.execute_redis_command(database.pool, "hget", "question", chat_id)
    question = variables.questions[int(index)]
    answer = variables.correct_answer_list[int(index)-1]
    return question, answer, int(index)

def send_welcome(bot):
    @bot.message_handler(commands=["start"])
    async def send_welcome(message: types.Message):
        chat_id = message.chat.id
        await database.execute_redis_command(database.pool, "hset", "score", chat_id, 0)
        await database.execute_redis_command(database.pool, "hset", "question", chat_id, 0)
        markup = types.InlineKeyboardMarkup()
        start_btn = types.InlineKeyboardButton(text="💸", callback_data="start_test_button_pushed")
        markup.add(start_btn)
        await bot.send_message(chat_id, variables.welcome_message_text, reply_markup=markup, parse_mode="HTML")

def send_question(bot):
    @bot.callback_query_handler(func=lambda call:True)
    async def query_handler(call):
        try:
            chat_id = call.message.chat.id
            current_user_question, correct_answer, index = await text_question_answer(chat_id)
            await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            if call.data == "start_test_button_pushed":
                markup = await buttons.buttons_creation()
                await bot.send_message(chat_id=chat_id, text=current_user_question, reply_markup=markup, parse_mode="HTML")
                await database.execute_redis_command(database.pool, "hset", "question", chat_id, index + 1)
            elif index == 10:
                if call.data == correct_answer:
                    current_score = await database.execute_redis_command(database.pool, "hget", "score", chat_id)
                    await bot.send_message(chat_id = chat_id, text= await variables.result_texts(int(current_score)+1), parse_mode="HTML")
                    await database.execute_redis_command(database.pool, "hdel", "question", chat_id)
                    await database.execute_redis_command(database.pool, "hdel", "score", chat_id)
                else:
                    current_score = await database.execute_redis_command(database.pool, "hget", "score", chat_id)
                    await bot.send_message(chat_id = chat_id, text= await variables.result_texts(int(current_score)), parse_mode="HTML")
                    await database.execute_redis_command(database.pool, "hdel", "question", chat_id)
                    await database.execute_redis_command(database.pool, "hdel", "score", chat_id)
            elif call.data == correct_answer:
                markup = await buttons.buttons_creation()
                current_score = await database.execute_redis_command(database.pool, "hget", "score", chat_id)
                await bot.send_message(chat_id=chat_id, text=current_user_question, reply_markup=markup, parse_mode="HTML")
                await database.execute_redis_command(database.pool, "hset", "score", chat_id, int(current_score) + 1)
                await database.execute_redis_command(database.pool, "hset", "question", chat_id, index + 1)
            else:
                markup = await buttons.buttons_creation()
                await bot.send_message(chat_id=chat_id, text=current_user_question, reply_markup=markup, parse_mode="HTML")
                await database.execute_redis_command(database.pool, "hset", "question", chat_id, index + 1)
            
            await bot.answer_callback_query(callback_query_id=call.id)
        
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"Я не знаю как обработать эту команду 👾\n\nПопробуй начать заново: /start", parse_mode="HTML")
            print(f"{e}=")






