from asyncpg.exceptions import ForeignKeyViolationError

from services.db import DatabaseConnection
from errors import DaoNotFoundUserError


class ScheduleDAO:

    def __init__(self, db: DatabaseConnection) -> None:
        self._db = db

    async def add_schedule(self, user_id: str, str_type: str, time_start: str, time_end: str) -> None:
        """
        add string to schedule or update string if str_type 'start' or 'end'
        :param user_id: user's id
        :param str_type: schedule string type ('start', 'end', 'eat', 'rest')
        :param time_start: start time string of schedule
        :param time_end: end time string of schedule
        :return:
        """
        async with self._db.pool.acquire() as conn:
            try:
                if str_type in ('start', 'end'):
                    await conn.execute("""
                        WITH res AS (
                            UPDATE schedule SET time_start=$3, time_end=$4
                            WHERE user_id=$1 and str_type=$2
                            RETURNING *
                        )
                        INSERT INTO schedule (user_id, str_type, time_start, time_end)
                        SELECT $1, $2, $3, $4
                        WHERE NOT EXISTS (SELECT * FROM res)
                    """, user_id, str_type, time_start, time_end)
                else:
                    await conn.execute("""
                        INSERT INTO schedule
                            (user_id, str_type, time_start, time_end)
                        VALUES
                            ($1, $2, $3, $4)
                    """, user_id, str_type, time_start, time_end)
            except ForeignKeyViolationError:
                raise DaoNotFoundUserError
