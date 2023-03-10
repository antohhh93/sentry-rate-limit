from ratelimit.db.base import Project

class ProjectDatabase:
    """
    Для работы с таблицей Project в базе данных.

    ProjectSubquery:
        вывод sql запроса:
        {'id': 1, 'project_sentry_id': '1', 'slug': 'testing', 'limit_id': 12}
    """

    def __init__(self, **kwargs):
        self.projects: list = []
        super().__init__(**kwargs)

    ProjectAlias = Project.alias()
    ProjectSubquery = (ProjectAlias
        .select(ProjectAlias)
        .order_by(ProjectAlias.id.asc())
        .alias('tProject')
    )

    def get_projects(self):
        for data_dict in (self.ProjectSubquery).dicts():
            self.projects.append(data_dict)
        
        return self.projects
