
class UrlConfig:
    def __init__(self, *, func=None, path=None, button=None,
                 details=False, permission=None, object_id_arg_name='object_id', **extra):
        self.func = func
        self.method = func.__name__
        self.path = path
        self.permission = permission
        self.details = details
        self.button = button
        self.object_id_arg_name = object_id_arg_name
        self.extra = extra

    def __repr__(self):
        return f'<UrlConfig func:"{self.func}" path:"{self.path}" button:"{self.button}">'
