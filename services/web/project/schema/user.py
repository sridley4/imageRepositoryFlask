from project.ma import ma
from project.models.users import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
