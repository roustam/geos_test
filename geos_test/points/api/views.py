from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from points.models import PointsModel, LinesModel
from .serializers import LocationSerializer
import haversine as hs
import networkx as nx

class PointPageView(APIView):
    def get(self, request, from_point):
        data = PointsModel.objects.get(obj_id=from_point)
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

        data = PointsModel.objects.filter(obj_id__in=calculation_result['shortest_path'])
        serializer = LocationSerializer(data, many=True)

        solved_response = {'shortest_distance': calculation_result['shortest_distance'],
                           'shortest_path': calculation_result['shortest_path'],
                           'total_score': calculation_result['total_score'],
                           'geo_points': serializer.data}
        return Response(solved_response)

def calculate_distances(point1, point2):
    # Haversine algorithm. Lon, lat coordinates must to be separated by a comma.
    return hs.haversine(point1, point2)


# converting ids and coordinates into convenient format
def get_points_dict():
    points_id = tuple(i.obj_id for i in PointsModel.objects.all())  # tuple with objects id
    point_coords = tuple(i.geom.tuple for i in PointsModel.objects.all())  # tuple with coordinates
    return dict(zip(points_id, point_coords))


def lines_data():
    lines = tuple(i for i in LinesModel.objects.all())
    return lines


def get_point_score(obj_id):
    score = PointsModel.objects.get(obj_id=obj_id)
    return score.score


# solving task with distance calculation - min_length
def solve_distance_task(get_from, get_to):
    MyGraph = nx.Graph()
    total_score = 0
    coordinates = get_points_dict()
    lines_len = lines_data()
    for i in lines_len:
        distance = calculate_distances(
            coordinates[i.get_from_id()],
            coordinates[i.get_to_id()]
        )
        MyGraph.add_edge(i.get_from_id(), i.get_to_id(), weight=distance)
    shortest_path = (nx.shortest_path(MyGraph, source=get_from, target=get_to, weight='weight'))
    shortest_distance = (nx.shortest_path_length(MyGraph, source=get_from, target=get_to, weight='weight'))
    for obj_id in shortest_path:
        total_score += get_point_score(obj_id)
    return {'shortest_distance': shortest_distance, 'shortest_path': shortest_path, 'total_score': total_score}


# solving task with point score values - min_score
def solve_score_task(get_from, get_to):
    MyGraph = nx.DiGraph()
    total_score = 0
    coordinates = get_points_dict()
    lines_len = lines_data()
    # making a directed graph
    for i in lines_len:
        MyGraph.add_edge(i.from_point.obj_id, i.to_point.obj_id, weight=i.from_point.score) # straight edges
        MyGraph.add_edge(i.to_point.obj_id, i.from_point.obj_id, weight=i.to_point.score) # reversed edges
    shortest_path = (nx.shortest_path(MyGraph, source=get_from, target=get_to, weight='weight'))
    shortest_distance = (nx.shortest_path_length(MyGraph, source=get_from, target=get_to, weight='weight'))
    for obj_id in shortest_path:
        total_score += get_point_score(obj_id)

    return {'shortest_distance': shortest_distance, 'shortest_path': shortest_path, 'total_score': total_score}


# function for testing purposes
def process_view(request):
    MyGraph = nx.Graph()
    if request.method == 'GET':
        coordinates = get_points_dict()
        lines_len = lines_data()
        # line_distances = calculate_distances()
        for i in lines_len:
            distance = calculate_distances(
                coordinates[i.get_from_id()],
                coordinates[i.get_to_id()]
            )
            MyGraph.add_edge(i.get_from_id(), i.get_to_id(), weight=distance)

        shortest_path = (nx.shortest_path(MyGraph, source=2, target=6, weight='weight'))
        shortest_distance = (nx.shortest_path_length(MyGraph, source=2, target=6, weight='weight'))
        total_score = 0
        for obj_id in shortest_path:
            total_score += get_point_score(obj_id)

        return HttpResponse(f'Наикратчайший маршрут {shortest_path} <br><br> Длинна {shortest_distance} км <br><br> кол-во баллов {total_score}')
    else:
        return HttpResponse('Method Not allowed')