from ratelimit.db import (
    model,
    Database,
)

class Project(Database):
    """
    Для синхронизации проектов из sentry и базы данных.

    delete_project_missing_in_sentry:
        удаляет проекты из базы данных, если их нет в senty

    create_project_in_database:
        проверяет что проектов из sentry нет в базе данных
        проверяет что проекты из sentry относятся к организации в базе данных
        добавляет проекты из sentry в базу данных
    """

    def __init__(self, sentry_projects: list = [], database_projects: list = [], database_organizations: list = [], **kwargs):
        self.sentry_projects = sentry_projects
        self.database_projects = database_projects
        self.database_organizations = database_organizations
        super().__init__(**kwargs)
    
    def delete_project_missing_in_sentry(self):
        for database_project_data in self.database_projects[:]:
            if all(database_project_data['project_sentry_id'] != sentry_project_data['id'] 
                        for sentry_project_data in self.sentry_projects):

                self.recursive_delete_id(model.Project, database_project_data['id'])

    def create_project_in_database(self):
        for sentry_project_data in self.sentry_projects[:]:
            if all(sentry_project_data['id'] != database_project_data['project_sentry_id'] 
                        for database_project_data in self.database_projects):
                if any(int(sentry_project_data['organization']['id']) == int(database_organization_data['organization_sentry_id']) 
                            for database_organization_data in self.database_organizations):

                    self.insert_one_row(model.Project, 
                                            project_sentry_id = sentry_project_data['id'],
                                            slug = sentry_project_data['slug']
                                        )
