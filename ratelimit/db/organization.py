from ratelimit.db.base import Organization

class OrganizationDatabase:
    """
    Для работы с таблицей Organization в базе данных.

    OrganizationSubquery:
        вывод sql запроса:
        {'id': 1, 'organization_sentry_id': '1', 'slug': 'testing', 'limit_id': 11}
    """

    def __init__(self, **kwargs):
        self.organizations: list = []
        super().__init__(**kwargs)

    OrganizationAlias = Organization.alias()
    OrganizationSubquery = (OrganizationAlias
        .select(OrganizationAlias)
        .order_by(OrganizationAlias.id.asc())
        .alias('tOrganization')
    )

    def get_organizations(self):
        for data_dict in (self.OrganizationSubquery).dicts():
            self.organizations.append(data_dict)
        
        return self.organizations
