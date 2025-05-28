# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/16 下午4:32
# @filename: model_factory
# @version : V1
# @description :

from models.location import Location
from models.score_detail import ScoreDetail
from models.user_preview import UserPreview
from models.way_point import WayPoint
from models.route_preview import RoutePreview, PickedRoutePreview
from models.traffic import Traffic


class ModelFactory:
    @staticmethod
    def create_model(model_type, **kwargs):
        models = {
            'location': Location,
            'user_preview': UserPreview,
            'way_point': WayPoint,
            'route_preview': RoutePreview,
            'picked_route_preview': PickedRoutePreview,
            'traffic': Traffic,
            'score_detail': ScoreDetail
        }
        model = models.get(model_type)()
        if model is None:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model

    @staticmethod
    def change_list_to_model(model_type, data: list):
        if data is None:
            return None
        return [ModelFactory.create_model(model_type, **d).info for d in data]

