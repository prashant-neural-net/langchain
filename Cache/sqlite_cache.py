import sqlite3
from pathlib import Path
from typing import Optional


class SQLiteCache:
    def __init__(self, database_path: str="cache.db"):
        self.database_path = Path(database_path)
        self._initialize_db()

    def _get_connection(self):
        return sqlite3.connect(self.database_path)

    def _initialize_db(self):
        with self._get_connection() as connection:
            connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS responses(
                cache_key TEXT PRIMARY KEY,
                prompt TEXT NOT NULL,
                model_name TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )

            connection.commit()

    def get(self, cache_key: str) -> Optional[str]:
        with self._get_connection() as connection:
            cursor = connection.execute(
                '''SELECT response 
                   from responses
                   where cache_key = ?
                   ''',
                   (cache_key,),
            )
            row = cursor.fetchone()

            if row is None:
                return None
            
            return row[0]
    
    def set(self, cache_key, prompt, model_name, response):
        with self._get_connection() as connection:
            connection.execute(
                '''
                INSERT OR REPLACE INTO responses
                (   cache_key,
                    prompt,
                    model_name,
                    response
                )
                VALUES(?, ?, ?, ?)
                ''',
                (cache_key, prompt, model_name, response),
            )

            connection.commit()

    def clear(self):
        with self._get_connection() as connection:
            connection.execute(
                '''
                    DELETE FROM responses
                    ''')
            
            connection.commit()

    def count(self) -> int:
        with self._get_connection() as connection:
            cursor = connection.execute(
                '''
                SELECT COUNT(*) FROM responses'''
            )
            return cursor.fetchone()[0]
            

    
