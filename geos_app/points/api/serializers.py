from rest_framework import serializers
from points.models import PointsModel, LinesModel
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class LineNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinesModel
        fields = ['line_id','from_point_id', 'to_point_id']


class LocationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PointsModel
        many = True
        geo_field = "geom"
        fields = ('id', 'score', 'city')

class LocationSerializerList(GeoFeatureModelSerializer):

    class Meta:
        model = PointsModel
        geo_field = "geom"
        fields = ('id', 'score', 'obj_id')

