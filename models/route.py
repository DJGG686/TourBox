# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/3 下午3:06
# @filename: route
# @version : V1
# @description :
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from database_connect.mysql_connector import MySQLConnector
from enumeration.table_enum import Table
from models import ROUTE_SEARCH_CONTENT
from models.base_model import BaseModel
from models.location import Location
from models.model_factory import ModelFactory
from models.page_limit import Page
from models.user_preview import UserPreview
from models.way_point import WayPoint
from util.file_util import delete_file, file_url
from util.sql_util import Condition
from util.uuid_util import generate_uuid


@dataclass
class Route(BaseModel):
    db_connector = MySQLConnector()
    route_id: Optional[int] = None
    user_id: Optional[str] = ''
    nickname: Optional[str] = ''
    avatar: Optional[str] = ''
    title: Optional[str] = ''
    cover: Optional[str] = ''
    description: Optional[str] = ''
    ispublic: Optional[int] = 1
    day_num: Optional[int] = 0
    location_num: Optional[int] = 0
    like_num: Optional[int] = 0
    lscore: Optional[float] = 0
    rscore: Optional[float] = 0
    tscore: Optional[float] = 0
    create_time: Optional[str] = datetime.now()
    update_time: Optional[str] = datetime.now()
    tag: Optional[List[int]] = None
    manager: Optional[List[UserPreview]] = None
    location: Optional[List[List[Location]]] = None
    way: Optional[List[List[WayPoint]]] = None
    traffic: Optional[List[List[List[WayPoint] | None]]] = None
    base_cities: Optional[List[str]] = None

    def __setattr__(self, key, value):
        if key == 'cover' or key == 'avatar' and value is not None:
            super().__setattr__(key, file_url(key, value))
        elif key == 'create_time' or key == 'update_time' and value is not None:
            super().__setattr__(key, value.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            super().__setattr__(key, value)

    def set_attr(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                self.__setattr__(key, value)

    @property
    def route_schema(self):
        return dict(user_id=self.user_id, title=self.title, description=self.description,
                    ispublic=self.ispublic, day_num=self.day_num, location_num=self.location_num,
                    update_time=self.update_time, create_time=self.create_time)

    def get_route_info(self):
        return self.get_route_info_by_route_id(self.route_id)

    def get_route_info_by_route_id(self, route_id: Optional[int] = None):
        result = self.db_connector.select(table=Table.route, columns=['route.*', 'user.nickname', 'user.avatar'],
                                          where=Condition().left_join('user', 'user_id')
                                          .equal('route_id', route_id), single=True)
        if result:
            self.set_attr(**result)
        else:
            return None
        # get tags
        self.tag = self.get_tags(route_id)
        # get manager
        self.manager = self.get_managers(route_id)
        # get location
        self.location = self.get_locations(route_id)
        # get way
        self.way = self.get_ways(route_id)
        # get traffic
        self.traffic = self.get_traffics(route_id)
        # get base_cities
        self.base_cities = self.get_base_cities(route_id)
        return self.info

    def get_tags(self, route_id: int):
        tags = self.db_connector.select(table=Table.tag,
                                        where=Condition().equal('route_id', route_id))
        if not tags:
            return []
        return [tag['tagcode'] for tag in tags]

    def get_managers(self, route_id: int):
        managers = self.db_connector.select(table=Table.manage,
                                            columns=['user.user_id', 'nickname', 'avatar', 'signature'],
                                            where=Condition().equal('route_id', route_id).left_join('user', 'user_id'))
        if not managers:
            return []
        return ModelFactory.change_list_to_model('user_preview', managers)

    def get_locations(self, route_id: int):
        locations = self.db_connector.select(table=Table.location, columns=['*'],
                                             where=Condition().equal('route_id', route_id))
        if not locations:
            return []
        result = defaultdict(list)
        for _location in locations:
            result[_location['list_id']].append(ModelFactory.create_model('location', **_location).info)
        return list(result.values())

    def get_ways(self, route_id: int):
        ways = self.db_connector.select(table=Table.way_list,
                                        where=Condition().left_join(Table.location, 'list_id')
                                        .equal(str(Table.way_list) + '.route_id', route_id))
        if not ways:
            return []
        result = defaultdict(list)
        for _way in ways:
            result[_way['list_id']].append(ModelFactory.create_model('way_point', **_way).info)
        return list(result.values())

    def get_traffics(self, route_id: int):
        traffic = self.db_connector.select(table=Table.way_list,
                                           where=Condition()
                                           .left_join(Table.polyline, 'traffic_id')
                                           .left_join(Table.traffic, 'list_id')
                                           .equal('route_id', route_id))
        if not traffic:
            return []
        result = defaultdict(list)
        for _traffic in traffic:
            seq_num = _traffic['seq_num']
            if seq_num is None:
                result[_traffic['list_id']].append([])
            else:
                way_point = ModelFactory.create_model('traffic', **_traffic).info
                if seq_num >= len(result[_traffic['list_id']]):
                    result[_traffic['list_id']].append([])
                    if _traffic.get('longitude') is not None:
                        way_point['polyline'] = dict(longitude=_traffic['longitude'], latitude=_traffic['latitude'])
                    result[_traffic['list_id']][seq_num].append(way_point)
                else:
                    result[_traffic['list_id']][seq_num].append(way_point)
        return list(result.values())

    def get_base_cities(self, route_id: int):
        result = self.db_connector.select(table=Table.base_cities, columns=['city'],
                                          where=Condition().equal('route_id', route_id))
        if not result:
            return []
        return [city['city'] for city in result]

    def update_cover(self):
        result = self.db_connector.select(table=Table.route, columns=['cover'],
                                          where=Condition().equal('route_id', self.route_id))
        if not result:
            return 'route not exist'
        if not self.db_connector.update(table=Table.route, data=dict(cover=self.cover),
                                        where=Condition().equal('route_id', self.route_id)):
            return 'cover update failed'
        if result['cover'] != 'default.jpeg':
            delete_file('cover', result['cover'])
        return None

    def search_routes(self, keyword: str, page: Page):
        result = self.db_connector.select(table=Table.route, columns=['route.*', 'user.nickname', 'user.avatar'],
                                          where=Condition().left_join(Table.user, 'user_id')
                                          .left_join(Table.location, 'route_id')
                                          .left_join(Table.base_cities, 'route_id')
                                          .or_like(ROUTE_SEARCH_CONTENT, keyword)
                                          .page(page))
        return ModelFactory.change_list_to_model('route_preview', result)

    def get_explore_routes(self, count: int = 10, tag: int = 0):
        result = self.db_connector.select(table=Table.route, columns=['route.*', 'user.nickname', 'user.avatar'],
                                          where=Condition().left_join(Table.user, 'user_id')
                                          .left_join(Table.tag, 'route_id')
                                          .equal('tagcode', tag, None if tag else 'select distinct tagcode from tag')
                                          .order_by('RAND()').limit(count))
        return ModelFactory.change_list_to_model('route_preview', result)

    def get_picked_routes(self, count: int = 10, tag: int = 0):
        result = self.db_connector.select(table=Table.picked,
                                          columns=['route.*', 'user.nickname', 'user.avatar', 'reason'],
                                          where=Condition().left_join(Table.user, 'user_id')
                                          .left_join(Table.tag, 'route_id')
                                          .left_join(Table.route, 'route_id')
                                          .equal('tagcode', tag, None if tag else 'select distinct tagcode from tag')
                                          .order_by('RAND()').limit(count))
        return ModelFactory.change_list_to_model('picked_route_preview', result)

    def insert_route(self):
        if not self.db_connector.insert(table=Table.route, data=self.route_schema):
            return 'insert failed'
        if (route_id := self.db_connector.get_last_insert_id()) is None:
            return 'sql error'
        for _tag in self.tag:
            if not self.db_connector.insert(table=Table.tag, data=dict(route_id=route_id, tagcode=_tag)):
                return 'tag insert failed'
        return {'route_id': route_id}

    def update_route(self, data: dict):
        if (result := self.db_connector.update(table=Table.route, data=data,
                                               where=Condition().equal('route_id', self.route_id))) is None:
            return 'update failed'
        return 'update success', result

    def update_tags(self, tags: List[int]):
        if self.db_connector.delete(table=Table.tag, where=Condition().equal('route_id', self.route_id)) is None:
            return 'tag delete failed'
        for _tag in tags:
            if self.db_connector.insert(table=Table.tag, data=dict(route_id=self.route_id, tagcode=_tag)) is None:
                return 'tag insert failed'
        return None

    def delete_route(self):
        if self.db_connector.delete(table=Table.route, where=Condition().equal('route_id', self.route_id)) is None:
            return 'delete failed'
        return None

    def add_location(self, location: List[List[dict]]):
        for _location in location:
            for _loc in _location:
                _loc['route_id'] = self.route_id
                if self.db_connector.insert(table=Table.location, data=_loc) is None:
                    return 'location insert failed'
        return None

    def update_location(self, location: List[List[dict]]):
        if self.db_connector.delete(table=Table.location, where=Condition().equal('route_id', self.route_id)) is None:
            return 'update location error'
        return self.add_location(location)

    def delete_location(self, location_to_delete: List[str]):
        for location in location_to_delete:
            if self.db_connector.delete(table=Table.location, where=Condition().equal('name', location)) is None:
                return 'location delete failed'
        return None

    def add_way(self, way: List[List[dict]]):
        for way_list in way:
            list_id = generate_uuid()
            self.db_connector.insert(table=Table.way_list, data=dict(route_id=self.route_id, list_id=list_id))
            for way_point in way_list:
                if (result := self.db_connector.update(table=Table.location, data=dict(list_id=list_id),
                                                       where=Condition().equal('route_id', self.route_id)
                                                       .and_condition().equal('name', way_point['name'])
                                                       .and_condition().equal('address', way_point['address']))) is None:
                    # 删除 way_list
                    self.db_connector.delete(table=Table.way_list, where=Condition().equal('list_id', list_id))
                    return 'way update failed'
                elif result == 0:
                    self.db_connector.delete(table=Table.way_list, where=Condition().equal('list_id', list_id))
                    return f'location: {way_point.get("name")} not found'
        return None

    def update_way(self, way: List[List[dict]]):
        if self.db_connector.delete(table=Table.way_list, where=Condition().equal('route_id', self.route_id)) is None:
            return 'update way error'
        return self.add_way(way)

    def add_traffic(self, traffic: List[List[List[dict]]] = None):
        way_list = self.db_connector.select(table=Table.way_list, columns=['list_id'],
                                            where=Condition().equal('route_id', self.route_id))
        if not way_list:
            return 'this route has no way yet'
        if len(way_list) != len(traffic):
            return 'traffic day num not match way day num'
        for i in range(len(traffic)):
            list_id = way_list[i]['list_id']
            for seq_num in range(len(traffic[i])):
                for _traffic in traffic[i][seq_num]:
                    to_insert = ModelFactory.create_model('traffic', **_traffic).info
                    to_insert['list_id'] = list_id
                    to_insert['seq_num'] = seq_num
                    if self.db_connector.insert(table=Table.traffic, data=to_insert) is None:
                        return 'traffic insert failed'
                    if (polyline := _traffic.get('polyline')) is not None:
                        traffic_id = self.db_connector.get_last_insert_id()
                        polyline['traffic_id'] = traffic_id
                        if self.db_connector.insert(table=Table.polyline, data=polyline) is None:
                            return 'polyline insert failed'
        return None

    def update_traffic(self, traffic: List[List[List[dict]]] = None):
        if self.db_connector.delete(table=Table.traffic, to_delete='traffic', where=Condition().left_join(Table.way_list, 'list_id').equal('route_id', self.route_id)) is None:
            return 'update traffic error'
        return self.add_traffic(traffic)


if __name__ == '__main__':
    route = Route(route_id=2, cover='default.jpeg')
    # print(route.get_route_info())
    # print(route.get_locations(2))
    # print(route.get_ways(2))
    # print(json.dumps(route.get_traffics(2), ensure_ascii=False, indent=4))
    # print(json.dumps(route.get_route_info(), ensure_ascii=False, indent=4))
    # a = route.get_route_info()
    # print(a)
    # print(json.dumps(a, ensure_ascii=False, indent=3))
    # with open('../route_demo.json', 'w', encoding='utf-8') as f:
    #     json.dump(a, f, ensure_ascii=False, indent=4)
    print(a := route.search_routes('上海', Page(1, 10)))
    print(json.dumps(a, ensure_ascii=False, indent=4))

