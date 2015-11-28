import resource

class Wood(resource.Resource):
    def __init__(self, image_path=None, bounds=None, pos=None, _map_=None,):
        resource.Resource.__init__(
            self,
            Container=Wood,
            resource_type="wood",
            bounds=bounds,
            pos=pos,
            _map_=_map_,
            worth=1,
        )
