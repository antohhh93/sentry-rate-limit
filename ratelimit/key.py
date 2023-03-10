from ratelimit.db import (
    model,
    Database,
)

class Key(Database):
    """
    Для синхронизации ключей из sentry и базы данных.

    delete_key_missing_in_sentry:
        удаляет ключи из базы данных, если их нет в senty

    create_new_key_in_database:
        проверяет что ключей из sentry нет в базе данных
        проверяет что ключи из sentry относятся к проекту в базе данных
        добавляет ключи из sentry в базу данных
    """

    def __init__(self, sentry_keys: list = [], database_keys: list = [], database_projects: list = [], **kwargs):
        self.sentry_keys = sentry_keys
        self.database_keys = database_keys
        self.database_projects = database_projects
        super().__init__(**kwargs)
    
    def delete_key_missing_in_sentry(self):
        for database_key_data in self.database_keys[:]:
            if all(database_key_data['key_sentry_id'] != sentry_key_data['id'] 
                        for sentry_key_data in self.sentry_keys):

                self.recursive_delete_id(model.Key, database_key_data['id'])

    def create_new_key_in_database(self):
        for sentry_key_data in self.sentry_keys[:]:
            if all(sentry_key_data['id'] != database_key_data['key_sentry_id'] 
                        for database_key_data in self.database_keys):
                if any(int(sentry_key_data['projectId']) == int(database_project_data['project_sentry_id']) 
                            for database_project_data in self.database_projects):

                    self.insert_one_row(model.Key, key_sentry_id = sentry_key_data['id'])

