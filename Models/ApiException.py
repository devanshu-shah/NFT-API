from werkzeug.exceptions import BadRequest
from functools import wraps
from route.Return import Return

def handleException(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            try_result = fun(*args, **kwargs)
            return try_result
        except KeyError as e:
            error_warning = {'error_warning': 'A key error has occurred. Please check if the keys of the uploaded json are correct.'}
            return jsonify(error_warning)
        except TypeError as e:
            error_warning = {'error_warning': 'A type error has occurred. Please check if the uploaded json data type is correct.'}
            return Return.returnResponse(error_warning,201)
        except BadRequest as e:
            return Return.returnResponse(e.data['message'],e.code)
        except Exception as e:
            error_warning = {'Some Internal Issue Occured ':repr(e)}
            return Return.returnResponse(error_warning,201)
    return wrapper
