from project.ma import ma
from project.models.albums import Album


class AlbumSchema(ma.ModelSchema):
    class Meta:
        model = Album