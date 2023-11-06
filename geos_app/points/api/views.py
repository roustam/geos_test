from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from points.models import PointsModel, LinesModel
from .serializers import LocationSerializer, LineNumberSerializer
from haversine import haversine, Unit
import networkx as nx
from django.db.models import Sum

class LinesPageView(APIView):
    def get(self, request):
        data = LinesModel.objects.all()
        serializer = LineNumberSerializer(data, many=True)
        print('ser-zer;', serializer)
        return Response(serializer.data)

class PointPageView(APIView):
    def get(self, request, from_point):
        data = PointsModel.objects.get(id=from_point)
        print(data)
        serializer = LocationSerializer(data)
        return Response(serializer.data)

class AllPointRecordsView(APIView):

    def get(self, request):
        data = PointsModel.objects.all()
        serializer = LocationSerializer(data, many=True)
        return Response(serializer.data)


class SendPointRecordsView(APIView):

    def get(self, request, from_point, to_point, method):
        if method == 'min_score':
            calculation_result = solve_score_task(from_point, to_point)
        elif method == 'min_length':
            calculation_result = solve_distance_task(from_point, to_point)
        else:
            raise Http404

        data = PointsModel.objects.filter(id__in=calculation_result['shortest_path'])
        serializer = LocationSerializer(data, many=True)

        solved_response = {'shortest_distance': calculation_result['shortest_distance'],
                           'shortest_path': calculation_result['shortest_path'],
                           'total_score': calculation_result['total_score'],
                           'geo_points': serializer.data}
        return Response(solved_response)

def calculate_distances(point1, point2):
    # Haversine algorithm. Lon, lat coordinates must to be separated by a comma.
    return haversine(point1, point2, unit=Unit.KILOMETERS)


# converting ids and coordinates into convenient format
def get_points_dict():
    points_id = tuple(i.id for i in PointsModel.objects.all())  # tuple with objects id
    point_coords = tuple(i.geom.tuple for i in PointsModel.objects.all())  # tuple with coordinates
    return dict(zip(points_id, point_coords))


def lines_data():
    lines = tuple(i for i in LinesModel.objects.all())
    return lines


def get_point_score(obj_id):
    score = PointsModel.objects.get(id=obj_id)
    return score.score

def get_km_distance(lines_list):
    total_distance = 0
    lines_recs = PointsModel.objects.filter(id__in=lines_list)
    if lines_recs.count() < 2:
        return 0
    else:
        for i in range(lines_recs.__len__()):
            if i < lines_recs.__len__() - 1:
                #print('>>  >>>', lines_recs[i].geom.coords, lines_recs[i+1].geom.coords)
                
                total_distance += haversine((lines_recs[i].geom.coords[1], lines_recs[i].geom.coords[0]),
                                            (lines_recs[i+1].geom.coords[1], lines_recs[i+1].geom.coords[0]))
        return total_distance

    
# solving task with distance calculation - min_length
def solve_distance_task(get_from, get_to):
    MyGraph = nx.Graph()
    total_score = 0
    coordinates = get_points_dict()
    lines_len = lines_data()


    for i in lines_len:
        # distance = calculate_distances(
        #     coordinates[i.from_point_id],
        #     coordinates[i.to_point_id]
        # )
        MyGraph.add_edge(i.from_point_id, i.to_point_id, weight='weight')
    shortest_path = (nx.shortest_path(MyGraph, source=get_from, target=get_to, weight='weigth'))
    

    shortest_distance = get_km_distance(shortest_path)
    return {'shortest_distance': shortest_distance, 'shortest_path': shortest_path, 'total_score': total_score}


# solving task with point score values - min_score
def solve_score_task(get_from, get_to):
    MyGraph = nx.DiGraph()
    total_score = 0

    lines_len = lines_data()
    # making a directed graph
    for i in lines_len:
        MyGraph.add_edge(i.from_point.id, i.to_point.id, weight=i.from_point.score) # straight edges
        MyGraph.add_edge(i.to_point.id, i.from_point.id, weight=i.to_point.score) # reversed edges
    shortest_path = (nx.shortest_path(MyGraph, source=get_from, target=get_to, weight='weight'))
    shortest_distance = (nx.shortest_path_length(MyGraph, source=get_from, target=get_to, weight='weight'))
    total_score=PointsModel.objects.filter(id__in=shortest_path).aggregate(sum=Sum('score'))
    print('total s core', total_score)
    total_score_sum = total_score['sum']


    return {'shortest_distance': shortest_distance, 'shortest_path': shortest_path, 'total_score': total_score_sum}