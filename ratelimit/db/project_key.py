from ratelimit.db.base import ProjectKey
from ratelimit.db.limit import LimitDatabase
from ratelimit.db.project import ProjectDatabase
from ratelimit.db.key import KeyDatabase

class ProjectKeyDatabase(LimitDatabase, ProjectDatabase, KeyDatabase):
    """
    Для работы с таблицей ProjectKey в базе данных.

    ProjectKeySubquery:
        вывод sql запроса:
        {'id': 1, 'project_id': 1, 'key_id': 1}

    ProjectKey_Project_Key:
        вывод sql запроса:
        {'project_id': 1, 'key_id': 1, 'project_sentry_id': '1', 'slug': 'testing', 'id': 1, 'key_sentry_id': '00000000000000000000000000000000', 'limit_id': 12}

    get_project_key:
        получает список всех проектов и их ключей
    
    creating_array_project_and_key:
        создает список из проектов и их ключей
        добавляет к проектам данные о лимитах
        добавляет к проектам список ключей
        добавляет к ключам данные о лимитах
    """

    def __init__(self, **kwargs):
        self.projects_keys: list = []
        self.project_list: list = []
        super().__init__(**kwargs)

    ProjectKeyAlias = ProjectKey.alias()
    ProjectKeySubquery = (ProjectKeyAlias
        .select(ProjectKeyAlias)
        .alias('tProjectKey')
    )

    ProjectKey_Project_Key = (ProjectKeyAlias
        .select(
            ProjectKeyAlias.project_id, 
            ProjectKeyAlias.key_id, 
            ProjectDatabase.ProjectAlias.project_sentry_id, 
            ProjectDatabase.ProjectAlias.slug, 
            KeyDatabase.KeyAlias
        )
        .join(ProjectDatabase.ProjectAlias)
        .switch()
        .join(KeyDatabase.KeyAlias)
    )

    def get_project_key(self):
        for data_dict in (self.ProjectKey_Project_Key).dicts():
            self.projects_keys.append(data_dict)
        
        return self.projects_keys

    def creating_array_project_and_key(self):
        for project_data in self.projects:
            details = project_data.copy()
            key_details = []

            for limit_data in self.limits:
                if project_data['limit_id'] == limit_data['id']:
                    details['limit'] = limit_data

            for project_key_data in self.projects_keys:
                if project_key_data['project_id'] == project_data['id']:
                    
                    for key_data in self.keys:
                        if project_key_data['key_id'] == key_data['id']:

                            for limit_data in self.limits:
                                if key_data['limit_id'] == limit_data['id']:
                                    key_data['limit'] = limit_data

                            key_details.append(key_data)

            details['keys'] = key_details
            self.project_list.append(details)
        
        return self.project_list
