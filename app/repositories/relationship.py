class RelationshipRepository:
    def __init__(self, database):
        self.database = database

    def save(
        self,
        source_id: int,
        target_id: int,
        relationship_type: str,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO relationships
                (
                    source_id,
                    target_id,
                    relationship_type
                )
                VALUES (?, ?, ?)
                """,
                (
                    source_id,
                    target_id,
                    relationship_type,
                ),
            )

            connection.commit()

    def find_related(
        self,
        source_id: int,
    ):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT resources.*
                FROM relationships
                JOIN resources
                ON resources.id = relationships.target_id
                WHERE relationships.source_id = ?
                """,
                (
                    source_id,
                ),
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]