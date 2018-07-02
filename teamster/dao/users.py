from typing import List
from asyncpg.exceptions import ForeignKeyViolationError
from asyncpg import Record

from services.db import DatabaseConnection


class UsersDAO:

    def __init__(self, db: DatabaseConnection) -> None:
        self._db = db

    async def create_user(self, name: str, birthday: str, phone: str, email: str) -> None:
        """
        create new user
        :param name: user name
        :param birthday: user birthday
        :param phone: user phone
        :param email: user email
        :return:
        """
        async with self._db.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users
                    (name, birthday, phone, email)
                VALUES
                    ($1, $2, $3 , $4)
            """, name, birthday, phone, email)

    async def get_user(self, user_id: str) -> Record:
        """
        get one user by id
        :param user_id: user id
        :return: user record
        """
        async with self._db.pool.acquire() as conn:
            user = await conn.fetchrow("""
                SELECT * FROM users
                WHERE id = $1
            """, user_id)
        return user

    async def get_users_list(self) -> List[Record]:
        """
        get list users with schedule
        :param:
        :return: users records
        """
        async with self._db.pool.acquire() as conn:
            await conn.set_type_codec("json", encoder=json.dumps, decoder=json.loads, schema='pg_catalog')
            users = await conn.fetch("""
                SELECT *,
                    row_to_json(SELECT * FROM schedule t WHERE t.user_id=users.id) schedule
                FROM users
            """)
        return user
