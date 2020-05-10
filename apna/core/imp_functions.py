from math import sin, cos, sqrt, atan2, radians


def distance_algo(la1, lo1, la2, lo2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(la1)
    lon1 = radians(lo1)
    lat2 = radians(la2)
    lon2 = radians(lo2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def getNearbyShops(customerLat, customerLong, shopLat, shopLon, approvedDistance):
    dist = distance_algo(customerLat, customerLong, shopLat, shopLon)
    print('dist')
    print(dist)
    print('approvedDistance')
    print(approvedDistance)
    if dist <= approvedDistance:
        return True
    return False


def getNearbyShopDistance(customerLat, customerLong, shopLat, shopLon):
    dist = distance_algo(customerLat, customerLong, shopLat, shopLon)
    return dist


def sortShopList(shopList, distanceList):
    # for i in range(0, len(shopList)):
    pass
