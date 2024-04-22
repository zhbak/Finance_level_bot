import time, asyncio
from bot_structure import handlers, config


    
handlers.send_welcome(config.bot)
handlers.send_question(config.bot)



async def main():
    await config.bot.polling()

if __name__ == "__main__":
    print('Bot started.')
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Exception occurred: {e}")
            time.sleep(15)  # Пауза перед следующей попыткой