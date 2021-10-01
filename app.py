from flask import Flask, json
from flask_restful import Api
from Route import Path

app = Flask(__name__)
#Adding secret_key 
app.config['SECRET_KEY'] = 'abcd'
app.debug=False
api=Api(app)
api.prefix='/api/v1'


if __name__=='__main__':
    #Adds all Resources of Controller
    Path.initalize_routes(api)
    app.run(debug=False)