from ratelimit.db.base import OrganizationProject
from ratelimit.db.limit import LimitDatabase
from ratelimit.db.project import ProjectDatabase
from ratelimit.db.organization import OrganizationDatabase

class OrganizationProjectDatabase(LimitDatabase, OrganizationDatabase, ProjectDatabase):
    """
    Для работы с таблицей OrganizationProject в базе данных.

    OrganizationProjectSubquery:
        вывод sql запроса:
        {'id': 1, 'organization_id': 1, 'project_id': 1}

    OrganizationProject_Organization_Project:
        вывод sql запроса:
        {'organization_id': 1, 'project_id': 1, 'organization_sentry_id': '1', 'id': 1, 'project_sentry_id': '1', 'slug': 'testing', 'limit_id': 12}

    get_organization_projects:
        получает список всех организаций и их проектов
    
    creating_array_organization_and_projects:
        создает список из организаций и их проектов
        добавляет к организациям данные о лимитах
        добавляет к организациям список проектов
        добавляет к проектам данные о лимитах
    """

    def __init__(self, **kwargs):
        self.organizations_projects: list = []
        self.organization_list: list = []
        super().__init__(**kwargs)

    OrganizationProjectAlias = OrganizationProject.alias()
    OrganizationProjectSubquery = (OrganizationProjectAlias
        .select(OrganizationProjectAlias)
        .alias('tOrganizationProject')
    )

    OrganizationProject_Organization_Project = (OrganizationProjectAlias
        .select(
            OrganizationProjectAlias.organization_id, 
            OrganizationProjectAlias.project_id, 
            OrganizationDatabase.OrganizationAlias.organization_sentry_id, 
            ProjectDatabase.ProjectAlias
        )
        .join(OrganizationDatabase.OrganizationAlias)
        .switch()
        .join(ProjectDatabase.ProjectAlias)
    )
    
    def get_organization_projects(self):
        for data_dict in (self.OrganizationProject_Organization_Project).dicts():
            self.organizations_projects.append(data_dict)
        
        return self.organizations_projects

    def creating_array_organization_and_projects(self):
        for organization_data in self.organizations:
            details = organization_data.copy()
            project_details = []

            for limit_data in self.limits:
                if organization_data['limit_id'] == limit_data['id']:
                    details['limit'] = limit_data

            for organization_project_data in self.organizations_projects:
                if organization_project_data['organization_id'] == organization_data['id']:

                    for project_data in self.projects:
                        if organization_project_data['project_id'] == project_data['id']:

                            for limit_data in self.limits:
                                if project_data['limit_id'] == limit_data['id']:
                                    project_data['limit'] = limit_data

                            project_details.append(project_data)
            
            details['projects'] = project_details
            self.organization_list.append(details)
        
        return self.organization_list
