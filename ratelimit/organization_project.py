from ratelimit.db import model
from ratelimit.project import Project

class OrganizationProject(Project):
    """
    Для создания зависимостей между организациями и проектами в базе данных.
    """

    def __init__(self, database_organizations_projects: list = [], **kwargs):
        self.database_organizations_projects = database_organizations_projects
        super().__init__(**kwargs)

    def create_dependency_between_organization_and_project(self):
        data_source: str = []
        for sentry_project_data in self.sentry_projects[:]:
            if 'organization_id' in locals(): del organization_id
            if 'project_id' in locals(): del project_id

            for database_project_data in self.database_projects:
                if int(sentry_project_data['id']) == int(database_project_data['project_sentry_id']):
                    project_id = database_project_data['id']

            if 'organization' in sentry_project_data:
                for database_organization_data in self.database_organizations:
                    if sentry_project_data['organization']['id'] == database_organization_data['organization_sentry_id']:
                        organization_id = database_organization_data['id']

            if 'organization_id' in locals() and 'project_id' in locals():
                if all(organization_id != database_organization_project_data['organization_id'] 
                            or project_id != database_organization_project_data['project_id'] 
                                for database_organization_project_data in self.database_organizations_projects):
                    data_source.append({"organization_id": organization_id, "project_id": project_id})

        self.insert_many_row(model.OrganizationProject, data_source)

