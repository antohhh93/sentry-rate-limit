import logging
from ratelimit.db.model import *
from ratelimit.config import DATABASE

logger = logging.getLogger()

def all_subclasses(base: type) -> list[type]:
    return [
        cls
        for sub in base.__subclasses__()
        for cls in [sub] + all_subclasses(sub)
    ]

models = [
    sub for sub in all_subclasses(BaseModel)
    if not sub.__name__.startswith('_')
]

class Database:
    """
    Для работы с базой данных.
    """

    def create_all_tables(self, table):
        """
        CREATE TABLE
        """
        try:
            with DATABASE.atomic():
                return DATABASE.create_tables(table)
        except Exception as exc:
            logger.exception("Exception occurred")

    def insert_many_row(self, table, data_source):
        """
        INSERT INTO
        """
        try:
            with DATABASE.atomic():
                for data_dict in data_source:
                    table.create(**data_dict)
        except Exception as exc:
            logger.exception("Exception occurred")
    
    def insert_one_row(self, table, **data_source):
        """
        INSERT INTO
        """
        try:
            with DATABASE.atomic():
                return table.insert(data_source).execute()
        except Exception as exc:
            logger.exception("Exception occurred")

    def recursive_delete_id(self, table, id):
        """
        DELETE
        """
        try:
            delete = table.get(table.id == id)
            return delete.delete_instance(recursive=True)
        except Exception as exc:
            logger.exception("Exception occurred")
    
    def update_limit(self, table, id, limit_id):
        """
        UPDATE LIMIT
        """
        try:
            update = table.update(limit_id=limit_id).where(table.id == id)
            return update.execute()
        except Exception as exc:
            logger.exception("Exception occurred")
