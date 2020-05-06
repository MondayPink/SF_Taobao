from django.db import models

# Create your models here.
class address_info(models.Model):
    longitude = models.FloatField() #经度
    latitude = models.FloatField()#维度
    data = models.CharField(max_length=200)# 标记被点击所触发的目标的内容
