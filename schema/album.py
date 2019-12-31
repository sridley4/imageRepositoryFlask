from ma import ma
from models.albums import Album


class AlbumSchema(ma.ModelSchema):
    class Meta:
        model = Album