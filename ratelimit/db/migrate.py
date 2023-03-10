import logging
from ratelimit.db.base import (
    Database,
    Limit,
)
from ratelimit.config import DEFAULT_LIMITS

logger = logging.getLogger()

class Migrations(Database):
    """
    Для добавления первоначальных данных в базу данных.
    """

    def apply_migration_limit(self):
        """Default data for the table Limit"""
        if Limit.select().count() == 0:
            return self.insert_many_row(Limit, DEFAULT_LIMITS)
        else:
            return logger.info("Migrations are not required.")
