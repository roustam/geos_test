from django.contrib.gis.db import models

class PointsModel(models.Model):
    id=models.AutoField(primary_key=True)
    obj_id = models.IntegerField(default=0)
    geom = models.PointField()
    score = models.IntegerField()

    def __str__(self):
        return str(self.obj_id)

class LinesModel(models.Model):
    line_id = models.AutoField(primary_key=True)
    from_point = models.ForeignKey(PointsModel, on_delete=models.CASCADE, related_name='from_point')
    to_point = models.ForeignKey(PointsModel, on_delete=models.CASCADE, related_name='to_point')

    # get point line ids as tuple
    def get_from_id(self):
        return self.from_point.obj_id

    def get_to_id(self):
        return self.to_point.obj_id

    def __str__(self):
        return str(self.line_id)
