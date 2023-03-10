from peewee import *
from ratelimit.config import DATABASE

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = DATABASE

class Limit(BaseModel):
    id = AutoField()
    count = IntegerField(null=False)
    window = IntegerField(default=60)
    description = TextField(null=True)
    fixed = BooleanField(default=False)

    class Meta:
        table_name = 'Limit'

class Organization(BaseModel):
    id = AutoField()
    organization_sentry_id = TextField(null=False)
    slug = TextField(null=False)
    limit_id = ForeignKeyField(Limit, related_name='organizations', default=1, null=True)

    class Meta:
        table_name = 'Organization'

class Project(BaseModel):
    id = AutoField()
    project_sentry_id = TextField(null=False)
    slug = TextField(null=False)
    limit_id = ForeignKeyField(Limit, related_name='projects', null=True)

    class Meta:
        table_name = 'Project'

class Key(BaseModel):
    id = AutoField()
    key_sentry_id = TextField(null=False)
    limit_id = ForeignKeyField(Limit, related_name='keys', null=True)

    class Meta:
        table_name = 'Key'

class OrganizationProject(BaseModel):
    id = AutoField()
    organization_id = ForeignKeyField(Organization, related_name='projects')
    project_id = ForeignKeyField(Project, related_name='organizations')

    class Meta:
        table_name = 'OrganizationProject'

class ProjectKey(BaseModel):
    id = AutoField()
    project_id = ForeignKeyField(Project, related_name='keys')
    key_id = ForeignKeyField(Key, related_name='projects')

    class Meta:
        table_name = 'ProjectKey'
