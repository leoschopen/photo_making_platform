import requests
import uuid


# 将具体的地址 转为经纬度
from bug_manage import settings


def getcode(site, city):
    parameters = {'address': site, 'city': city, 'key': settings.GAODE_COS_KEY}
    base_url = 'https://restapi.amap.com/v3/geocode/geo'
    response = requests.get(url=base_url, params=parameters)
    info_site = response.json()
    return info_site['geocodes'][0]['location']
    # print(info_site['geocodes'][0]['location'])


# 将经纬度 转化为 具体的地址
def lo_to_addr(location):
    parameters = {'location': location, 'key': settings.GAODE_COS_KEY}
    base_url = 'https://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(url=base_url, params=parameters)
    info_site = response.json()
    # return info_site
    return info_site['regeocode']['formatted_address']
    # print(info_site['regeocode']['formatted_address'])


if __name__ == '__main__':
    # 具体的地址，在包含城市的情况下 city 可以为空
    address = '广东省深圳市南山区桃源街道龙珠六路'
    # 城市
    city = ''
    location = getcode(address, city)
    address_from_location = lo_to_addr("113.980836777953,22.566142254795")

    print('根据输入的地址获取到的经纬度为：', location)
    print('根据经纬度得到的地址为：', address_from_location)
    print(location.split(',')[0])