from ratelimit.request import Request
from ratelimit.config import (
    SENTRY_URL, 
    SENTRY_API_URL,
)

class ProjectGetSentry(Request):
    """
    Для работы с проектами из sentry.

    get_projects:
        получает список всех проектов 
        преобразовывает полученные данные (оставляет только id, slug, organization)
        преобразовывает данные об организации (оставляет только id, slug)
    """

    def __init__(self, **kwargs):
        self.projects: list = []
        super().__init__(**kwargs)

    def get_projects(self, url = SENTRY_URL + SENTRY_API_URL['projects']):
        response = self.get(url)
        for project in response:
            for name in list(project):
                if name not in ['id', 'slug', 'organization']:
                    project.pop(name)
            for name in list(project['organization']):
                if name not in ['id', 'slug']:
                    project['organization'].pop(name)
            self.projects.append(project)
        
        return self.projects
