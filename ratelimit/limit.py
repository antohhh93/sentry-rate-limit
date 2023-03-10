from ratelimit.db import model
from ratelimit.organization_project import OrganizationProject
from ratelimit.project_key import ProjectKey
from ratelimit.request import Request
from ratelimit.config import (
    SENTRY_URL,
    SENTRY_API_URL,
)

class Limit(Request, OrganizationProject, ProjectKey):
    """
    Для работы с лимитами в базе данных и в sentry.

    check_and_create_limit:
        проверяет наличие нового значения лимита в базе данных
        добавляет новое значение в базу данных если его нет
        проверяет наличие нового значения лимита в фиксированных лимитах базы данных
        получает id если значения нет в фиксированных лимитах
        добавляет новое значение в базу данных если есть только фиксированные лимиты
    
    update_limit_to_project:
        распределяет лимит организации на проекты
        проверяет сумму фиксированных лимитов проектов
        обновляет лимит (лимит == 1 сообщению в минуту на проект) в проектах без фиксированных значений, если лимит организации исчерпан
        распределяет оставшийся доступный лимит на проект
        обновляет лимиты в проектах без фиксированных значений

    update_limit_to_key:
        распределяет лимит проекта на ключи
        проверяет сумму фиксированных лимитов ключей
        обновляет лимит (лимит == 1 сообщению в минуту на ключ) в ключах без фиксированных значений, если лимит проекта исчерпан
        распределяет оставшийся доступный лимит на ключи
        обновляет лимиты в ключах без фиксированных значений

    update_limit_key_to_sentry:
        собирает запрос подставляя нужные данные из базы данных
        обновляет лимиты ключей в sentry
    """

    def __init__(self, database_limits: list = [], **kwargs):
        self.database_limits = database_limits
        super().__init__(**kwargs)

    def check_and_create_limit(self, count, window):
        if all(count != database_limit_data['count']
                    for database_limit_data in self.database_limits):
            return  self.insert_one_row(model.Limit, 
                        count=count, 
                        window=window, 
                        description='Automatic creation'
                    )
        else:
            limits_with_unfixed: list = []
            for database_limit_data in self.database_limits[:]:
                if not database_limit_data['fixed']:
                    limits_with_unfixed.append(database_limit_data)

            for limit_data in limits_with_unfixed:
                if count == limit_data['count']:
                    return limit_data['id']
            
            if all(count != limit_data['count']
                    for limit_data in limits_with_unfixed):
                return  self.insert_one_row(model.Limit, 
                            count=count, 
                            window=window, 
                            description='Automatic creation'
                        )

    def update_limit_to_project(self):
        for organization_data in self.database_organizations_projects:
            projects_count: int = len(organization_data['projects'])
            projects: list = organization_data['projects']

            fixed_project: list = []

            for project_data in projects[:]:
                if project_data['limit_id']:
                    if project_data['limit']['fixed']:
                        fixed_project.append(project_data)
                        projects.remove(project_data)

            count_fixed_project: int = len(fixed_project)
            sum_fixed_limit_project: int = sum(project_data['limit']['count'] for project_data in fixed_project)

            left_projects_count: int = (projects_count - count_fixed_project)
            
            #TODO передалать на min_limit_count
            if sum_fixed_limit_project >= organization_data['limit']['count']:
                for project_data in projects:
                    if project_data['limit_id'] != 1:
                        self.update_limit(model.Project, 
                                id = project_data['id'],
                                limit_id = 1
                            )
            else:
                remaining_limit: int = round((organization_data['limit']['count'] - sum_fixed_limit_project) / (left_projects_count if left_projects_count > 0 else 1))

                #TODO передалать на min_limit_count
                limit_id = self.check_and_create_limit(
                                    count = remaining_limit if remaining_limit > 0 else 1, 
                                    window = organization_data['limit']['window']
                                )
                
                for project_data in projects:
                    self.update_limit(model.Project, 
                            id = project_data['id'], 
                            limit_id = limit_id
                        )

    def update_limit_to_key(self):
        for project_data in self.database_projects_keys:
            keys_count: int = len(project_data['keys'])
            keys: list = project_data['keys']

            fixed_keys: list = []

            for key_data in keys[:]:
                if key_data['limit_id']:
                    if key_data['limit']['fixed']:
                        fixed_keys.append(key_data)
                        keys.remove(key_data)
            
            count_fixed_key: int = len(fixed_keys)
            sum_fixed_limit_key: int = sum(key_data['limit']['count'] for key_data in fixed_keys)

            left_keys_count: int = (keys_count - count_fixed_key)

            #TODO передалать на min_limit_count
            if sum_fixed_limit_key >= project_data['limit']['count']:
                for key_data in keys:
                    if key_data['limit_id'] != 1:
                        self.update_limit(model.Key, 
                                id = key_data['id'],
                                limit_id = 1
                            )
            else:
                remaining_limit: int = round((project_data['limit']['count'] - sum_fixed_limit_key) / (left_keys_count if left_keys_count > 0 else 1))

                #TODO передалать на min_limit_count
                limit_id = self.check_and_create_limit(
                                    count = remaining_limit if remaining_limit > 0 else 1, 
                                    window = project_data['limit']['window']
                                )
                
                for key_data in keys:
                    self.update_limit(model.Key, 
                            id = key_data['id'], 
                            limit_id = limit_id
                        )

    def update_limit_key_to_sentry(self, url = SENTRY_URL + SENTRY_API_URL['key_id']):
        for organizations_projects_data in self.database_organizations_projects:
            for projects_data in organizations_projects_data['projects']:
                for project_key_data in self.database_projects_keys:
                    if projects_data['project_sentry_id'] == project_key_data['project_sentry_id']:

                        limit = [limit_data for limit_data in self.database_limits if project_key_data['limit_id'] == limit_data['id']][0]
                        data = {"rateLimit": {"count": limit['count'], "window": limit['window']} }
                        
                        response = self.put(url.format(
                                                    organization_slug = organizations_projects_data['slug'],
                                                    project_slug = projects_data['slug'],
                                                    key_id = project_key_data['key_sentry_id']
                                                ), 
                                                data = data
                                            )
                        #TODO добавить вывод результата в логгер

