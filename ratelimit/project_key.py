from ratelimit.db import model
from ratelimit.key import Key

class ProjectKey(Key):
    """
    Для создания зависимостей между проектами и ключами в базе данных.
    """

    def __init__(self, database_projects_keys: list = [], **kwargs):
        self.database_projects_keys = database_projects_keys
        super().__init__(**kwargs)

    def create_dependency_between_project_and_key(self):
        data_source: str = []
        for sentry_key_data in self.sentry_keys[:]:
            if 'key_id' in locals(): del key_id
            if 'project_id' in locals(): del project_id

            for database_key_data in self.database_keys:
                if sentry_key_data['id'] == database_key_data['key_sentry_id']:
                    key_id = database_key_data['id']
            
            for database_project_data in self.database_projects:
                if sentry_key_data['projectId'] == int(database_project_data['project_sentry_id']):
                    project_id = database_project_data['id']

            if 'key_id' in locals() and 'project_id' in locals():
                if all(project_id != database_project_key_data['project_id'] 
                            or key_id != database_project_key_data['key_id'] 
                                for database_project_key_data in self.database_projects_keys):
                    data_source.append({"project_id": project_id, "key_id": key_id})

        self.insert_many_row(model.ProjectKey, data_source)
