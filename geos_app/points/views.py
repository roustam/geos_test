from django.http import HttpResponse, HttpResponseBadRequest
from .models import PointsModel, LinesModel
import urllib.request
import json
from django.contrib.gis.geos import GEOSGeometry
from django.template.response import TemplateResponse


def index_view(request):
    all_points = PointsModel.objects.count()
    all_lines = LinesModel.objects.count()
    print(all_points, all_lines)
    if request.method == 'GET':
        return TemplateResponse(request,"base.html",{"all_lines": all_lines,"all_points":all_points })
    else:
        return HttpResponseBadRequest('Method not allowed')


# adding points data to database
def add_points(json_points):
    for point in json_points:
        #obj_id = point['obj_id']
        lat = point['lat']
        lon = point['lon']
        #score = point['score']
        geometry_obj = GEOSGeometry(f'POINT({lat} {lon})')
        new_point = PointsModel.objects.create(
            obj_id=point['obj_id'],
            geom = geometry_obj,
            score=point['score']
        )
        new_point.save()
        print(lat, lon)


# adding lines data to database
def add_lines(json_lines):
    for line in json_lines:
        print(line['from_obj'], line['to_obj'])
        line_start = PointsModel.objects.get(obj_id=line['from_obj'])
        line_end = PointsModel.objects.get(obj_id=line['to_obj'])
        new_line = LinesModel.objects.create(
            from_point=line_start,
            to_point=line_end
        )
        new_line.save()

