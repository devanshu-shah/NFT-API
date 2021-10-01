from Models.Constant import Constant
from Route.Functions import Function
from flask_restful import request

class JWTRequestFilter:
    @staticmethod
    def checkToken():
        reqpath=request.path
        if(reqpath!=None):
            if(JWTRequestFilter.isJWTRequired(reqpath)):
                if(JWTRequestFilter.checkJWTToken()):
                    
                    tokenObj=Function.validateToken()
                                     
                    return tokenObj;
                else:
                    return "INVALID:NOTOKEN"
            else:
                return None
        else:
            return "INVALID:LOGIN"

    @staticmethod
    def isJWTRequired(reqpath):
        if(reqpath==Constant.ADMIN_LOGIN_URL):
            return False
        else:
            return True
    @staticmethod
    def checkJWTToken():
        token=request.headers.get("token")
        if(token==None):
            return False
        return True