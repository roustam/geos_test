from django.http import HttpResponse
from .models import PointsModel, LinesModel
import urllib.request
import json
from django.contrib.gis.geos import GEOSGeometry



def index_view(request):
    data_source_url = "https://datum-test-task.firebaseio.com/api/lines-points.json"
    if request.method == 'GET':
        with urllib.request.urlopen(data_source_url) as url:
            response = url.read()
            charset = url.info().get_content_charset('utf-8')
            data = json.loads(response.decode(charset))
            json_lines = data['lines']
            json_points = data['points']
            if PointsModel.objects.count() == 0:
                add_points(json_points)
                add_lines(json_lines)
                return HttpResponse(f'New data has been added to DB.<br><br> Response :<br> lines {json_lines} <br><br> points {json_points}')
            else:
                return HttpResponse(f'Database already has the data.<br><br> Response :<br> lines {json_lines} <br><br> points {json_points}')
    else:
        return HttpResponse('rest test')


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

