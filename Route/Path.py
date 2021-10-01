import sys
import inspect
from Controller.AdminUser import *
from flask_restful import Resource
def initalize_routes(api):
    #adding Resources to api with Required menthods
    api.add_resource(AdminUser, "/adminuser/", methods=['GET', 'POST','PUT','DELETE'])
    api.add_resource(User, "/user/", methods=['GET', 'POST','PUT','DELETE'])

    return api