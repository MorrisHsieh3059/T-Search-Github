from get_functions import history_point_data, getDistance, get_yymm
from data_process import data_process

def min_distance(path, U):
    '''
        MIN_DISTANCE
            Type : Dictionary
            Keys : International ID of each typhoon, 'i' in essay
            Value: (dict) Dik, the min distance for ith typhoon to kth predicted point, for all j

            {
                "typhoon_international_id" : {
                    'point_k1': (float),
                    'point_k2': (float),
                    ,...
                }
            }
    '''
    min_distance = {}
    point_data = history_point_data(path) # get historical typhoon points, P(i,j) in essay

    for i in point_data: # i refers to the ith historic typhoon
        distance_ijk = {}

        for k in U:
            min = 10 ** 10
            for j in point_data[i]:
                # calulate the minimum distance (lat_ij, long_ij, lat_k, long_k)
                if getDistance(j[0], j[1], U[k]['latitude'], U[k]['longitude']) < min:
                    min = getDistance(j[0], j[1], U[k]['latitude'], U[k]['longitude'])

            distance_ijk[k] = min
        min_distance[i] = distance_ijk

    print('MIN DISTANCE SUCCESS!')
    return min_distance

def weight_of_all(path, U, w):
    '''
        WEIGHT_OF_ALL
            Type : List
                ith:
                    0: typhoon_international_id
                    1: <Route Score> sigma(k = 1, M) [1 + kw, k, 1] | for all Dik < radius
                    2: <Time  Score> [year, month]

            [
                [ 'typhoon_international_id', sigma[1 + kw, k, 1], [year, month] ]
            ]
    '''
    temp = {} # key: typhoon name; Value: sigma(1 + k * w)
    min_dist = min_distance(path, U)
    point_data = history_point_data(path)

    ### Part 1. Route Score
    for i in point_data:
        score = [0, 0, 0] # sigma[total, k, 1]
        count = 1 # kth

        # Whether the min distance(Dik) is less than radius
        for k in U:
            if min_dist[i][k] < U[k]['radius']:
                score[2] += 1
                score[1] += count
            count += 1 # kth predicted

        # Route score of ith typhoon
        score[0] = score[2] + score[1] * w
        temp[i] = score

    ### Part 2. Time Score
    yymm_data = get_yymm(path)
    weight_of_all = [ [i, temp[i], yymm_data[i]] for i in temp ]

    print('WEIGHT OF ALL SUCCESS!')
    return weight_of_all

def radix_sort(path, U, w = 1, n = 10):
    '''
        RADIX_SORT
            Type : Dictionary
            Keys : Priority of the approximate historic typhoons
            Value: typhoon_internation_id
    '''
    import datetime
    weight = weight_of_all(path, U, w)
    point_data = history_point_data(path)
    data = data_process(path)

    ### Part 1. Sort by the year (the closer, the more prior)
    for i in range(len(weight) - 1, 0, -1):
        for j in range(i):
            if weight[j][2][0] < weight[j + 1][2][0]:
                ret = weight[j]
                weight[j] = weight[j + 1]
                weight[j + 1] = ret

    ### Part 2. Sort by the month (the closer, the more prior)
    month = datetime.datetime.now().month
    for i in range(len(weight) - 1, 0, -1):
        for j in range(i):
            if abs(weight[j][2][1] - month) > abs(weight[j + 1][2][1] - month):
                ret = weight[j]
                weight[j] = weight[j + 1]
                weight[j + 1] = ret

    ### Part 3. Sort by the route score (the higher, the more prior), S(1 + kw) > S(k) > S(1), S = Sigma
    for k in range(2, -1, -1):
        for i in range(len(weight) - 1, 0, -1):
            for j in range(i):
                if weight[j][1][k] < weight[j + 1][1][k]:
                    ret = weight[j]
                    weight[j] = weight[j + 1]
                    weight[j + 1] = ret

    ### Part 4. output
    final = {}
    for i in range(n):
        typhoon_id = weight[i][0]
        name = data[typhoon_id]['header']['name']

        json_point_data = []
        for j in point_data[typhoon_id]:
            lat = j[0]
            lon = j[1]
            temp = {"latitude": lat, "longitude": lon}
            json_point_data.append(temp)

        final[i + 1] = {"name": name, "id": typhoon_id, "points": json_point_data}

    print('RADIX SORT SUCCESS!')
    return final
