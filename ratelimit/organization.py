from ratelimit.db import (
    model,
    Database,
)

class Organization(Database):
    """
    Для синхронизации организаций из sentry и базы данных.

    delete_organization_missing_in_sentry:
        удаляет организации из базы данных, если их нет в senty
    """

    def __init__(self, sentry_organizations: list = [], database_organizations: list = [], **kwargs):
        self.sentry_organizations = sentry_organizations
        self.database_organizations = database_organizations
        super().__init__(**kwargs)

    def delete_organization_missing_in_sentry(self):
        for database_organization_data in self.database_organizations[:]:
            if all(database_organization_data['organization_sentry_id'] != sentry_organization_data['id'] 
                        for sentry_organization_data in self.sentry_organizations):

                self.recursive_delete_id(model.Organization, database_organization_data['id'])
