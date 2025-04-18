from flask_restx import Namespace, Resource

misc_ns = Namespace('', description='Misc endpoints')

@misc_ns.route('/')
class Root(Resource):
    def get(self):
        return {"message": "Welcome to ReCircle API!"}
