class BaseResponse:
    safe_response_status_code = [200, 201, 202, 203, 204, 400]
    success_status_code = [200, 201, 202, 203, 204]
    fail_status_code = [400]
    _success_handle = 'get_success_response'
    _fail_handle = 'get_fail_response'

    def get_default_response(self, request, response, *args, **kwargs):
        # 修改默认的请求响应的行为
        if self.is_safe_response(response):
            status_code = response.status_code
            handle = self._success_handle if status_code in self.success_status_code else self._fail_handle
            response = getattr(self, handle)(request, response, *args, **kwargs)
        return response

    def is_safe_response(self, response):
        # 判断请求是否为需要继续处理的请求对象
        return response.status_code in self.safe_response_status_code

    def get_success_response(self, request, response, *args, **kwargs):
        raise NotImplementedError()

    def get_fail_response(self, request, response, *args, **kwargs):
        raise NotImplementedError()


class DefaultResponse(BaseResponse):
    # 可以在自己的视图里面修改返回的关键字参数,或者修改`get_errors`方法
    error_code = 'code'
    error_msg_code = 'errmsgs'

    def get_success_response(self, request, response, *args, **kwargs):
        # 默认的处理请求成功的处理函数
        # 如果要修改默认行为,请重写`get_success_data`
        return self.get_success_data(request, response, *args, **kwargs)

    def get_fail_response(self, request, response, *args, **kwargs):
        # 默认的处理请求失败的处理函数
        # 如果要修改默认行为,请重写`get_error_data`
        return self.get_error_data(request, response, *args, **kwargs)

    def get_success_data(self, request, response, *args, **kwargs):
        try:
            # 这里如果得到的不是分页过的response会抛出`AttributeError`,在全局设置里面将`PAGE_SIZE`设置好即可
            response.data.update({'success': True})
        except AttributeError:
            return response
        return response

    def get_error_data(self, request, response, *args, **kwargs):
        # 处理请求错误的(400状态码的响应)的默认方法
        errors = self.get_errors(request, response, *args, **kwargs)
        response.data = {'success': False, 'errors': errors}
        return response

    def get_errors(self, request, response, *args, **kwargs):
        # 将错误的信息封装成一个列表返回
        errors = list()
        errors_code = self.error_code
        error_msg_code = self.error_msg_code
        for code, errmsgs in response.data.items():
            item = dict()
            item[errors_code] = code
            item[error_msg_code] = errmsgs
            errors.append(item)
        return errors