from ratelimit.db.base import Key

class KeyDatabase:
    """
    Для работы с таблицей Key в базе данных.

    KeySubquery:
        вывод sql запроса:
        {'id': 1, 'key_sentry_id': '00000000000000000000000000000000', 'limit_id': 12}
    """

    def __init__(self, **kwargs):
        self.keys: list = []
        super().__init__(**kwargs)

    KeyAlias = Key.alias()
    KeySubquery = (KeyAlias
        .select(KeyAlias)
        .order_by(KeyAlias.id.asc())
        .alias('tKey')
    )

    def get_keys(self):
        for data_dict in (self.KeySubquery).dicts():
            self.keys.append(data_dict)
        
        return self.keys
