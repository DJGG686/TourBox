# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2024/10/23 上午12:38
# @filename: data_check
# @version : V1
# @description :


def is_location(location):
    if not isinstance(location, dict):
        return False
    if set(location.keys()) != {'name', 'address', 'latitude', 'longitude'}:
        return False
    if not isinstance(location['latitude'], float) or not isinstance(location['longitude'], float):
        return False
    return True


def is_way_point(way_point):
    if not isinstance(way_point, dict):
        return False
    if set(way_point.keys()) != {'name', 'address', 'latitude', 'longitude', 'round_time'}:
        return False
    if not isinstance(way_point['latitude'], float) or not isinstance(way_point['longitude'], float):
        return False
    return True


def check_data(func, data):
    if not isinstance(data, list):
        print("data is not a list")
        return False
    for item in data:
        if not isinstance(item, list):
            print(f"item {item} is not a list")
            return False
        for location in item:
            if not func(location):
                print(f"location {location} is not valid")
                return False
    return True


def is_traffic(traffic):
    if not isinstance(traffic, list):
        return False
    for item in traffic:
        if not isinstance(item, dict):
            return False
        if set(item.keys()) != {'approach', 'begin', 'end', 'cost', 'polyline'} and set(item.keys()) != {'approach', 'begin', 'end', 'cost'}:
            return False
        if item.get('polyline'):
            if not isinstance(item['polyline'], dict):
                return False
            if set(item['polyline'].keys()) != {'longitude', 'latitude'}:
                return False
            if not isinstance(item['polyline']['latitude'], float) or not isinstance(item['polyline']['longitude'], float):
                return False
    return True


def check_location(data):
    return check_data(is_location, data)


def check_way_point(data):
    return check_data(is_way_point, data)


def check_traffic(data):
    return check_data(is_traffic, data)

