class DefaultResponse:
    # 可以在自己的视图里面修改返回的关键字参数,或者修改`get_errors`方法
    error_code = 'code'
    error_msg_code = 'errmsgs'

    def get_success_handle(self, request, response, *args, **kwargs):
        try:
            # 这里如果得到的不是分页过的response会抛出`AttributeError`,在全局设置里面将`PAGE_SIZE`设置好即可
            response.data.update({'success': True})
            return response
        except AttributeError:
            return response

    def get_fail_handle(self, request, response, *args, **kwargs):
        errors = self.get_errors(request, response, *args, **kwargs)
        response.data = {'success': False, 'errors': errors}
        return response

    def get_errors(self, request, response, *args, **kwargs):
        errors = list()
        errors_code = self.error_code
        error_msg_code = self.error_msg_code
        for code, errmsgs in response.data.items():
            item = dict()
            item[errors_code] = code
            item[error_msg_code] = errmsgs
            errors.append(item)
        return errors
