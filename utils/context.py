class BaseContext:
    def __init__(self):
        self.request = None
        self.format = None
        self.view = None

    def set_context(self, serializer_field):
        context = serializer_field.context
        self.request = context.get('request')
        self.format = context.get('format')
        self.view = context.get('view')

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        raise NotImplemented()
