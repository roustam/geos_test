from typing import Any
from django.core.management.base import BaseCommand
import json
from os.path import join
from geos_test.settings import BASE_DIR
from points.models import PointsModel, LinesModel
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

class Command(BaseCommand):
    help = 'Add sample data with coordinates and lines weights.'

    def create_points_from_json(self):
        json_file_path = join(BASE_DIR, 'sample_points.json')
        f = open(json_file_path)
        data = json.load(f)
        
        for point in data['points']:
            print(point['city'], point['lat'], point['lon'])
            lat = point['lat']
            lon = point['lon']
            geometry_obj = GEOSGeometry(f'POINT({lon} {lat})')
            PointsModel.objects.create(
                geom = geometry_obj,
                score=point['score'],
                city=point['city'],
            )
        

        

    def create_lines(self):
    
        lines_list = (
            ('Moscow', 'Minsk'),('Moscow', 'Voronezh'), ('Astana','Moscow'),
            ('Astana', 'Voronezh'), ('Voronezh', 'Minsk'), ('Minsk', 'Berlin'), ('Berlin', 'Madrid'),
            ('Madrid', 'Rome'), ('Madrid', 'Alger'),('Alger', 'Casablanka'), ('Alger', 'Rome'),('Rome','Larnaka'),
            ('Larnaka', 'Baku'), ('Baku','Astana'),('Astana','Novosibirsk'),('Novosibirsk','Surgut'),('Surgut', 'Moscow'),
            ('Novosibirsk','Moscow'),('Casablanka','Madrid')
        )
        

        for city_connection in lines_list:
            from_city = PointsModel.objects.get(city=city_connection[0])
            to_city = PointsModel.objects.get(city=city_connection[1])
            LinesModel.objects.create(from_point=from_city, to_point=to_city)
            print('line created')


    def handle(self, *args: Any, **options: Any) -> str | None:
        points_qty = PointsModel.objects.count()
        lines_qty = LinesModel.objects.count()
        if not points_qty:
            self.create_points_from_json()
        if not lines_qty:
            self.create_lines()