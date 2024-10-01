from peewee import CharField, IntegerField, ForeignKeyField
from ..dbmodels.core import BaseModel
from ..modules.users.users import Users as CVTUsers
from ..modules.users.roles import Roles as CVTRoles
from ..modules.users.roles import Role
from ..modules.users.users import User

users = CVTUsers()
roles = CVTRoles()

class Roles(BaseModel):

    identifier = CharField(unique=True, max_length=16)
    name = CharField(unique=True, max_length=32)
    level = IntegerField()

    @classmethod
    def create(cls, name:str, level:int, identifier:str)->tuple:
        
        name = name.upper()

        if cls.name_exist(name):

            return None, f"role {name} is already used"

        if cls.identifier_exist(identifier):
                
            return None, f"identifier {identifier} is already used"
        
        query = cls(name=name, level=level, identifier=identifier)
        query.save()
        
        return query, f"Role creation successful"

    @classmethod
    def read_by_name(cls, name:str):
      
        return cls.get_or_none(name=name.upper())
    
    @classmethod
    def read_by_identifier(cls, identifier:str):
      
        return cls.get_or_none(identifier=identifier)

    @classmethod
    def name_exist(cls, name:str)->bool:
        
        return True if cls.get_or_none(name=name.upper()) else False
    
    @classmethod
    def identifier_exist(cls, identifier:str)->bool:

        return True if cls.get_or_none(identifier=identifier) else False
    
    @classmethod
    def read_names(cls)->list:

        return [role.name for role in cls.select()]
    
    @classmethod
    def fill_cvt_roles(cls):
        r"""
        Documentation here
        """
        for role in cls.select():

            _role = Role(
                name=role.name,
                level=role.level,
                identifier=role.identifier
            )

            roles.add(role=_role)

    def serialize(self)->dict:
        r"""
        Serialize database record to a jsonable object
        """

        return {
            "id": self.id,
            "identifier": self.identifier,
            "name": self.name,
            "level": self.level
        }


class Users(BaseModel):

    identifier = CharField(unique=True, max_length=16)
    username = CharField(unique=True, max_length=64)
    role = ForeignKeyField(Roles, backref='users', on_delete='CASCADE')
    email = CharField(unique=True, max_length=128)
    password = CharField(unique=True)
    name = CharField(unique=True, max_length=64, null=True)
    lastname = CharField(unique=True, max_length=64, null=True)

    @classmethod
    def create(cls, user:User)-> dict:

        if cls.username_exist(user.username):

            return None, f"username {user.username} is already used"

        if cls.email_exist(user.email):

            return None, f"email {user.email} is already used"
        
        if cls.identifier_exist(user.identifier):

            return None, f"identifier {user.identifier} is already used"
        
        query = cls(
            username=user.username,
            role=Roles.read_by_name(name=user.role.name),
            email=user.email,
            password=user.password,
            identifier=user.identifier,
            name=user.name,
            lastname=user.lastname
            )
        query.save()

        return query, f"User creation successful"

    @classmethod
    def read_by_username(cls, username:str):
   
        return cls.get_or_none(username=username)

    @classmethod
    def read_by_name(cls, name:str):
   
        return cls.get_or_none(name=name)

    @classmethod
    def name_exist(cls, name:str)->bool:

        return True if cls.get_or_none(name=name) else False
    
    @classmethod
    def username_exist(cls, username:str)->bool:

        return True if cls.get_or_none(username=username) else False
    
    @classmethod
    def email_exist(cls, email:str)->bool:

        return True if cls.get_or_none(email=email) else False
    
    @classmethod
    def identifier_exist(cls, identifier:str)->bool:

        return True if cls.get_or_none(identifier=identifier) else False
    
    @classmethod
    def fill_cvt_users(cls):
        r"""
        Documentation here
        """
        for user in cls.select():

            users.signup(
                username=user.username,
                role_name=user.role.name,
                email=user.email,
                password=user.password,
                name=user.name,
                lastname=user.lastname,
                identifier=user.identifier,
                encode_password=False
            )

    def serialize(self)-> dict:
        r"""
        Serialize database record to a jsonable object
        """

        return {
            "id": self.id,
            "identifier": self.identifier,
            "username": self.username,
            "email": self.email,
            "role": self.role.serialize(),
            "name": self.name,
            "lastname": self.lastname
        }