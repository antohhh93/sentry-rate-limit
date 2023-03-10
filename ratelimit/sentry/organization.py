from ratelimit.request import Request
from ratelimit.config import (
    SENTRY_URL, 
    SENTRY_API_URL,
)

class OrganizationGetSentry(Request):
    """
    Для работы с организациями из sentry.

    get_organizations:
        получает список всех организаций 
        преобразовывает полученные данные (оставляет только id, slug)
    """

    def __init__(self, **kwargs):
        self.organizations: list = []
        super().__init__(**kwargs)

    def get_organizations(self, url = SENTRY_URL + SENTRY_API_URL['organizations']):
        response = self.get(url)
        for organization in response:
            for name in list(organization):
                if name not in ['id', 'slug']:
                    organization.pop(name)
            self.organizations.append(organization)
        
        return self.organizations
