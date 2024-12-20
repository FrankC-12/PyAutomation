from flask import request
from flask_restx import Namespace, Resource, fields
from .... import PyAutomation
from ....extensions.api import api
from ....extensions import _api as Api
from ....modules.users.users import Users as CVTUsers
from ....dbmodels.users import Users


ns = Namespace('Users', description='Users')
app = PyAutomation()
users = CVTUsers()


login_model = api.model("login_model", {
    'username': fields.String(required=False, description='Username'),
    'email': fields.String(required=False, description='Email'),
    'password': fields.String(required=True, description='Password')
})

signup_model = api.model("signup_model", {
    'username': fields.String(required=True, description='Username'),
    'role_name': fields.String(required=True, description="Role ['operator', 'supervisor', 'admin', 'auditor']"),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'name': fields.String(required=False, description='User`s name'),
    'lastname':fields.String(required=False, description='User`s last name')
})

@ns.route('/')
class UsersResource(Resource):

    @api.doc(security='apikey')
    @Api.token_required(auth=True)
    def get(self):
        """Get all usernames"""

        return users.serialize(), 200

@ns.route('/signup')
class SignUpResource(Resource):
    
    @ns.expect(signup_model)
    def post(self):
        """User signup"""
        user, message = app.signup(**api.payload)
        
        if user:

            return user.serialize(), 200
        
        return message, 400


@ns.route('/login')
class LoginResource(Resource):


    @ns.expect(login_model)
    def post(self):
        """User login"""
        user, message = app.login(**api.payload)
        # user, message = users.login(**api.payload)

        if user:

            return {
                "apiKey": user.token,
                "role": user.role.name,
                "role_level": user.role.level
                }, 200

        return message, 403
    

@ns.route('/credentials_are_valid')
class VerifyCredentialsResource(Resource):
    
    @api.doc(security='apikey')
    @Api.token_required(auth=True)
    @ns.expect(login_model)
    def post(self):
        """Verify user credentials"""
        credentials_valid, _ = users.verify_credentials(**api.payload)
        return credentials_valid, 200
    
@ns.route('/<username>')
class UserResource(Resource):
    
    @api.doc(security='apikey')
    @Api.token_required(auth=True)
    def get(self, username):
        """Get user information"""
        
        user = users.get_by_username(username=username)

        if user:

            return user.serialize(), 200

        return f"{username} is not a valid username", 400

    # @api.doc(security='apikey')
    # @Api.token_required(auth=True)
    # def delete(self, username):
    #     """Delete user"""

    #     if users.delete_by_username(username=username):

    #         return {'message': f"User {username} deleted successfully"}, 200

    #     return {'message': f"{username} is not a valid username"}, 400


@ns.route('/logout')
class LogoutResource(Resource):

    @api.doc(security='apikey')
    @Api.token_required(auth=True)
    def post(self):
        """User logout"""
        if 'X-API-KEY' in request.headers:
                            
            token = request.headers['X-API-KEY']

        elif 'Authorization' in request.headers:
            
            token = request.headers['Authorization'].split('Token ')[-1]
        
        _, message = Users.logout(token=token)

        return message, 200