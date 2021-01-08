from http import HTTPStatus


class AppError(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def to_dict(self):
        error_type = self.__class__.__name__
        try:
            return {'error': {error_type: ''.join(self.args)}}
        except TypeError:
            return {'error': {error_type: self.args[0]}}

