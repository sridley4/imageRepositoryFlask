from ma import ma

class AlbumCreateRequest(ma.Schema):
    title = ma.String()
    image_id = ma.Integer()
    image_id_list = ma.Pluck("self", "image_id", many=True)


