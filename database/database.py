from redis.asyncio import ConnectionPool, Redis
from database.config import redis_host, redis_port, redis_username, redis_password

pool = ConnectionPool(host=redis_host, port=redis_port, username=redis_username, password=redis_password, decode_responses=True)

# redis executor
async def execute_redis_command(redis_pool, command: str, *args, **kwargs):
    """ Выполняет указанную команду Redis с переданными аргументами.
    Args:
        command (str): Название команды Redis, например 'get', 'set', 'del' и т.д.
        args: Позиционные аргументы для команды.
        kwargs: Именованные аргументы для команды.
    """
    async with Redis.from_pool(connection_pool=redis_pool) as redis:
        try:
            # Динамически вызываем метод из объекта Redis
            method = getattr(redis, command)
            result = await method(*args, **kwargs)  # Выполнение команды с аргументами
            return result
        except AttributeError:
            print(f"Redis does not support '{command}' method.")
            return None
        except Exception as e:
            print(f"Error executing Redis command '{command}': {e}")
            return None
        
    # Примеры использования
    #print(await execute_redis_command('get', 'some_key'))   # Получение значения по ключу
    #print(await execute_redis_command('set', 'some_key', 'new_value'))  # Установка значения
    #print(await execute_redis_command('del', 'some_key'))  # Удаление ключа