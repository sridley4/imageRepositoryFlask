from ma import ma
from models.images import Image


class ImageSchema(ma.ModelSchema):
    class Meta:
        model = Image
