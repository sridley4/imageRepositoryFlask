from ma import ma
from models.users import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
