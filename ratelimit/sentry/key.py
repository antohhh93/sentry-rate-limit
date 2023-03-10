from ratelimit.request import Request
from ratelimit.config import (
    SENTRY_URL, 
    SENTRY_API_URL,
)

class KeyGetSentry(Request):
    """
    Для работы с ключами из sentry. Список ключей формируется на данных из базы данных.

    get_project_keys:
        собирает запрос подставляя нужные данные
        получает список всех ключей 
        преобразовывает полученные данные (оставляет только id, projectId, rateLimit)
    """

    def __init__(self, organizations_with_projects: list = [], **kwargs):
        self.organizations_with_projects = organizations_with_projects
        self.keys: list = []
        super().__init__(**kwargs)

    def get_project_keys(self, url = SENTRY_URL + SENTRY_API_URL['key']):
        for organization in self.organizations_with_projects:
            for project in organization['projects']:

                response = self.get(url.format(organization_slug = organization['slug'], project_slug = project['slug']))

                for key in response:
                        for name in list(key):
                            if name not in ['id', 'projectId', 'rateLimit']:
                                key.pop(name)
                        self.keys.append(key)

        return self.keys
