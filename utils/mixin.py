from django_filters.utils import get_all_model_fields

ALL_FIELDS = '__all__'


class ApiViewMinxin:
    def dispatch(self, request, *args, **kwargs):
        # 执行父类的dispath,获取框架的处理的响应结构
        response = super(ApiViewMinxin, self).dispatch(request, *args, **kwargs)
        # 开始分发响应对象
        response = self.get_process_response(request, response, *args, **kwargs)
        # 返回应答
        return response

    def get_process_response(self, request, response, *args, **kwargs):
        # 发出处理对象
        handle = getattr(self, f'process_{self.process_key(request)}', self.get_default_response)
        # 处理应答
        response = handle(request, response, *args, **kwargs)
        return response

    def process_key(self, request):
        return request.method.lower()

    def get_default_response(self, request, response, *args, **kwargs):
        return response


class ViewSetMixIn(ApiViewMinxin):

    def process_key(self, request):
        return self.action
