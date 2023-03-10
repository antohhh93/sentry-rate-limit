from ratelimit.db.base import Limit

class LimitDatabase:
    """
    Для работы с таблицей Limit в базе данных.

    LimitSubquery:
        вывод sql запроса:
        {'id': 1, 'count': 1, 'window': 60, 'description': 'Default reserved value', 'fixed': False}
    """

    def __init__(self, **kwargs):
        self.limits: list = []
        super().__init__(**kwargs)

    LimitAlias = Limit.alias()
    LimitSubquery = (LimitAlias
        .select(LimitAlias)
        .order_by(LimitAlias.id.asc())
        .alias('tLimit')
    )

    def get_limit(self):
        for data_dict in (self.LimitSubquery).dicts():
            self.limits.append(data_dict)
        
        return self.limits
