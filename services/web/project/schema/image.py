from project.ma import ma
from project.models.images import Image


class ImageSchema(ma.ModelSchema):
    class Meta:
        model = Image
