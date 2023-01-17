from django.db import models

class CityInfo(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

class SeoulRouteInfo(models.Model):
    route_id = models.IntegerField(primary_key=True)
    route_type = models.CharField(max_length=10)
    route_name = models.CharField(max_length=30)
    company = models.CharField(max_length=128)
    first_stop = models.CharField(max_length=128)
    last_stop = models.CharField(max_length=128)
    time_first = models.CharField(max_length=14)
    time_last = models.CharField(max_length=14)
    length = models.FloatField()
    interval = models.IntegerField()

class SeoulBusInfo(models.Model):
    bus_id = models.IntegerField(primary_key=True)
    bus_type = models.CharField(max_length=1)
    route_id = models.IntegerField()
    update_time = models.DateField(auto_now=True)
    bus_number = models.CharField(max_length=128)
    gpsX = models.CharField(max_length=32)
    gpsY = models.CharField(max_length=32)
    congestion = models.CharField(max_length=1)
    isRunning = models.CharField(max_length=3)
    isFull = models.CharField(max_length=3)

class BusanRouteInfo(models.Model):
    lineid = models.CharField(max_length=15, primary_key=True)
    buslinenum = models.CharField(max_length=30)
    bustype = models.CharField(max_length=20)
    companyid = models.CharField(max_length=70)
    startpoint = models.CharField(max_length=40)
    endpoint = models.CharField(max_length=40)
    firsttime = models.CharField(max_length=30)
    endtime = models.CharField(max_length=30)
    headway = models.CharField(max_length=10)

class BusanBusInfo(models.Model):
    carno = models.CharField(max_length=10, primary_key=True)
    lineno = models.CharField(max_length=10)
    bstopnm = models.CharField(max_length=50)
    lowplate = models.CharField(max_length=4)
    gpsym = models.CharField(max_length=10)
    lin = models.CharField(max_length=10)
    lat = models.CharField(max_length=10)
    isRunning = models.CharField(max_length=3)

class NationRouteInfo(models.Model):
    routeid = models.CharField(max_length=30, primary_key=True)
    city = models.ForeignKey(CityInfo, on_delete=models.CASCADE)
    routeno = models.CharField(max_length=30)
    routetp = models.CharField(max_length=10)
    endnodenm = models.CharField(max_length=30)
    startnodenm = models.CharField(max_length=30)
    endvehicletime = models.CharField(max_length=4)
    startvehicletime = models.CharField(max_length=4)

class NationBusInfo(models.Model):
    routeid = models.CharField(max_length=30)
    routenm = models.CharField(max_length=30)
    vehicleno = models.CharField(max_length=10, primary_key=True)
    routetp = models.CharField(max_length=10)
    nodenm = models.CharField(max_length=30)
    gpslati = models.CharField(max_length=20)
    gpslong = models.CharField(max_length=20)
    isRunning = models.CharField(max_length=3, default='No')

