from typing import Any
from django.core.management.base import BaseCommand
import json
from os.path import join
from geos_test.settings import BASE_DIR
from points.models import PointsModel
from django.contrib.gis.geos import GEOSGeometry

class Command(BaseCommand):
    help = 'Add sample data with coordinates and lines weights.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        id_num=0
        json_file_path = join(BASE_DIR, 'sample_points.json')
        f = open(json_file_path)
        data = json.load(f)
        
        for point in data['points']:
            print(point, point['lat'], point['lon'])
            lat = point['lat']
            lon = point['lon']
            geometry_obj = GEOSGeometry(f'POINT({lat} {lon})')
            new_point = PointsModel.objects.create(
                geom = geometry_obj,
                score=point['score']
            )
            new_point.save()
