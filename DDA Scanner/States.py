from aiogram.dispatcher.storage import BaseStorage
import asyncpg

class PostgresStateStorage(BaseStorage):

    def __init__(self, **database_config):
        self.database_config = database_config

    async def create_connection(self):
        return await asyncpg.connect(**self.database_config)

    async def get_state(self, *, chat: int = None, user: int = None, default: str = None) -> str:
        user_id = user or chat
        conn = await self.create_connection()
        state = await conn.fetchval('SELECT state FROM user_settings WHERE user_id = $1', user_id)
        await conn.close()
        return state or default

    async def set_state(self, *, chat: int = None, user: int = None, state: str = None):
        user_id = user or chat
        conn = await self.create_connection()
        await conn.execute('UPDATE user_settings SET state = $2 WHERE user_id = $1', user_id, state)
        await conn.close()

    async def reset_state(self, *, chat: int = None, user: int = None, with_data: bool = False):
        await self.set_state(chat=chat, user=user, state=None)
        if with_data:
            await self.set_data(chat, {})

    async def set_data(self, chat: int, data: dict):
        pass

    async def get_data(self, *, chat: int = None, user: int = None) -> dict:
        return {}
