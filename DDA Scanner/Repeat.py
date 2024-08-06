import hashlib, aiocron
from Config import create_connection

async def add_hash(user_id, message):
    hash_value = hashlib.sha256((str(user_id) + message).encode()).hexdigest()

    query = "INSERT INTO repeat_messages (hash_value) VALUES ($1) ON CONFLICT DO NOTHING"

    conn = await create_connection()
    await conn.execute(query, hash_value)
    await conn.close()


async def hash_filter(user_id, message):
    hash_value = hashlib.sha256((str(user_id) + message).encode()).hexdigest()

    conn = await create_connection()
    result = await conn.fetchval('SELECT hash_value FROM repeat_messages WHERE hash_value = $1', hash_value)
    await conn.close()

    if result:
        return False
    else:
        return True

async def clear_all_records():
    conn = await create_connection()
    await conn.execute('DELETE FROM repeat_messages')
    await conn.close()

@aiocron.crontab('0 0 1 * *')
async def scheduled_task():
    await clear_all_records()
