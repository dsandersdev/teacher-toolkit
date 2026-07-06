from datetime import datetime


class ResourceRepository:
    def __init__(self, database):
        self.database = database

    def save(
        self,
        teacher_id: int,
        resource_type: str,
        title: str,
        content: str,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO resources
                (
                    teacher_id,
                    type,
                    title,
                    content,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    teacher_id,
                    resource_type,
                    title,
                    content,
                    datetime.now().isoformat(),
                ),
            )

            connection.commit()

            return cursor.lastrowid

    def get(self, resource_id: int):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM resources
                WHERE id = ?
                """,
                (resource_id,),
            )

            row = cursor.fetchone()

            if not row:
                return None

            return dict(row)

    def search(self, query: str = ""):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            query = query.strip()

            if not query:
                cursor.execute(
                    """
                    SELECT *
                    FROM resources
                    ORDER BY created_at DESC
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT *
                    FROM resources
                    WHERE title LIKE ?
                    OR content LIKE ?
                    OR type LIKE ?
                    ORDER BY created_at DESC
                    """,
                    (
                        f"%{query}%",
                        f"%{query}%",
                        f"%{query}%",
                    ),
                )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

            
            
    def find_by_type(
        self,
        resource_type: str,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT *
                FROM resources
                WHERE type = ?
                ORDER BY created_at DESC
                """,
                (
                    resource_type,
                ),
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]