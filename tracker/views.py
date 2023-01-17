from django.shortcuts import render

from django.core import serializers
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from urllib.request import Request, urlopen
from urllib.parse import urlencode

import xml.etree.ElementTree as ET
import json

from .models import CityInfo, SeoulRouteInfo, SeoulBusInfo, BusanRouteInfo, BusanBusInfo, NationRouteInfo, NationBusInfo

myKey = '9fT1NKVjG3WAtj6SkSkMQElAZiZG2jrNNl%2BCJ%2By%2FowQe%2Fllf6o2Z3tAwQhnzUuwTGMdoS6cSyZvu%2FBeIvr%2BVpA%3D%3D' 

def home(request):
    return render(request, 'home.html')

def db(request):
    return render(request, 'updateDB.html')

def seoul_route(request):
    routes = SeoulRouteInfo.objects.all()
    context = {'routes' : routes}

    return render(request, 'seoulroute.html', context)

def busan_route(request):
    routes = BusanRouteInfo.objects.all()
    context = {'routes' : routes}

    return render(request, 'busanroute.html', context)

def nation_route(request):
    cities = CityInfo.objects.all()
    context = {'cities': cities}

    return render(request, 'nationroute.html', context)

def nation_route_detail(request, city_code):
    city = CityInfo.objects.get(code=city_code)
    routes = NationRouteInfo.objects.filter(city__code=city_code)

    context = {'city': city, 'routes': routes}

    return render(request, 'nationroutedetail.html', context)

def seoul_company(request):
    routes = SeoulRouteInfo.objects.all()
    companies = SeoulRouteInfo.objects.values_list('company',flat=True).distinct()

    context = {'routes' : routes, 'companies' : companies}
    return render(request, 'seoulcompany.html', context)

def busan_company(request):
    routes = BusanRouteInfo.objects.all()
    companies = BusanRouteInfo.objects.values_list('companyid',flat=True).distinct()

    context = {'routes' : routes, 'companies' : companies}
    return render(request, 'busancompany.html', context)

def nation_company(request):
    cities = CityInfo.objects.all()

    context = {'cities': cities}
    return render(request, 'nationcompany.html', context)

def nation_company_detail(request, city_code):
    cities = CityInfo.objects.all()
    routes = NationRouteInfo.objects.filter(city__code=city_code)

    context = {'cities': cities, 'routes': routes}
    return render(request, 'nationcompanydetail.html', context)

def get_city_code(request):
    if request.method == 'POST':
        url = 'http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getCtyCodeList'
        params = '?serviceKey=' + myKey + '&_type=' + 'xml'
        request = Request(url + params)
        request.get_method = lambda : 'GET'

        try:
            response_body = urlopen(request).read()
            root = ET.fromstring(response_body)
            head_code = root.find('./header/resultCode').text
            if head_code == '00':
                total_items = len(root.findall('./body/items/item'))
                for item in root.findall('./body/items/item'):
                    city_code = int(item.find('citycode').text)
                    city_name = item.find('cityname').text
                    q = CityInfo(code=city_code, name=city_name)
                    q.save()

            context = {
                    'result': total_items,
                    }
            return JsonResponse(context)

        except:
            pass

def get_seoul_route(request):
    if request.method == 'POST':
        url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList'
        params = '?serviceKey=' + myKey + '&_type=' + 'xml'
        request = Request(url + params)
        request.get_method = lambda : 'GET'

        try:
            response_body = urlopen(request).read()
            root = ET.fromstring(response_body)
            head_code = root.find('./msgHeader/headerCd').text
            if head_code == '0':
                total_items = len(root.findall('./msgBody/itemList'))
                for item in root.findall('./msgBody/itemList'):
                    route_id = int(item.find('busRouteId').text)
                    route_type = get_seoul_type(int(item.find('routeType').text))
                    route_name = item.find('busRouteNm').text
                    company = item.find('corpNm').text
                    first_stop = item.find('stStationNm').text
                    last_stop = item.find('edStationNm').text
                    time_first = item.find('firstBusTm').text
                    time_last = item.find('lastBusTm').text
                    length = item.find('length').text
                    interval = item.find('term').text

                    q = SeoulRouteInfo(
                            route_id = route_id,
                            route_type = route_type,
                            route_name = route_name,
                            company = company,
                            first_stop = first_stop,
                            last_stop = last_stop,
                            time_first = time_first,
                            time_last = time_last,
                            length = length,
                            interval = interval
                            )
                    q.save()

            context = { 'result' : total_items,}
            return JsonResponse(context)

        except:
            pass

def get_busan_route(request):
    if request.method == 'POST':
        url = 'http://apis.data.go.kr/6260000/BusanBIMS/busInfo'
        params = '?serviceKey=' + myKey
        request = Request(url + params)
        request.get_method = lambda : 'GET'

        try:
            response_body = urlopen(request).read()
            root = ET.fromstring(response_body)
            head_code = root.find('./header/resultCode').text
            if head_code == '00':
                total_items = len(root.findall('./body/items/item'))
                for item in root.findall('./body/items/item'):
                    lineid = item.find('li.neid').text
                    bustype = item.find('bustype').text
                    buslinenum = item.find('buslinenum').text
                    companyid = item.find('companyid').text
                    startpoint = item.find('startpoint').text
                    endpoint = item.find('endpoint').text
                    try:
                        firsttime = item.find('firsttime').text
                    except:
                        firsttime = 'N/A'
                    try:
                        endtime = item.find('endtime').text
                    except:
                        endtime = 'N/A'
                    try:
                        headway = item.find('headwaynorm').text
                    except:
                        headway = 'N/A'

                    q = BusanRouteInfo(
                            lineid = lineid,
                            bustype = bustype,
                            buslinenum = buslinenum,
                            companyid = companyid,
                            startpoint = startpoint,
                            endpoint = endpoint,
                            firsttime = firsttime,
                            endtime = endtime,
                            headway = headway
                            )
                    q.save()

            context = { 'result' : total_items,}
            return JsonResponse(context)

        except:
            pass

def get_nation_route(request):
    if request.method == 'POST':
        url = 'http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteNoList'
        
        q1 = CityInfo.objects.all()
        count = 0
        for qq in q1:
            city_code = str(qq.code)
            city_name = qq.name

            params = '?serviceKey=' + myKey + '&_type=xml&numOfRows=1000' + '&cityCode=' + city_code
            request = Request(url + params)
            request.get_method = lambda : 'GET'
            try:
                response_body = urlopen(request).read()
                root = ET.fromstring(response_body)
                head_code = root.find('./header/resultCode').text
                if head_code == '00':
                    total_items = len(root.findall('./body/items/item'))
                    count += 1
                    print('{}:{}-{}'.format(count,city_name,total_items))
                    for item in root.findall('./body/items/item'):
                        routeid = item.find('routeid').text
                        q2 = CityInfo(code=int(city_code), name=city_name)
                        cityname = city_name
                        routeno = item.find('routeno').text
                        routetp = item.find('routetp').text
                        endnodenm = item.find('endnodenm').text
                        startnodenm = item.find('startnodenm').text
                        endvehicletime = item.find('endvehicletime').text
                        startvehicletime = item.find('startvehicletime').text
                        
                        q = NationRouteInfo(
                                routeid = routeid,
                                city = q2,
                                routeno = routeno,
                                routetp = routetp,
                                endnodenm = endnodenm,
                                startnodenm = startnodenm,
                                endvehicletime = endvehicletime,
                                startvehicletime = startvehicletime
                                )
                        q.save()
            except:
                pass

        context = { 'result' : count,}
        return JsonResponse(context)

def get_seoul_bus(request):
    if request.method == 'POST':
        url = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid'
        route = request.POST['message']
        params = '?serviceKey=' + myKey + '&busRouteId=' + route + '&_type=' + 'xml'
        request = Request(url + params)
        request.get_method = lambda : 'GET'

        q1 = SeoulBusInfo.objects.filter(route_id=route)
        for qq in q1:
            qq.isRunning = "No"
            qq.save()

        try:
            response_body = urlopen(request).read()
            root = ET.fromstring(response_body)
            head_code = root.find('./msgHeader/headerCd').text
            if head_code == '0':
                total_items = len(root.findall('./msgBody/itemList'))
                print(total_items)
                bus_route = int(route)
                for item in root.findall('./msgBody/itemList'):
                    bus_id = int(item.find('vehId').text)
                    if item.find('busType').text == '1':
                        bus_type = '일반'
                    else:
                        bus_type = '저상'

                    bus_number = item.find('plainNo').text
                    gpsX = item.find('gpsX').text
                    gpsY = item.find('gpsY').text
                    congestion = getCongestion(int(item.find('congetion').text))

                    if item.find('isrunyn').text == '1':
                        isRunning = 'Yes'
                    else:
                        isRunning = 'No'

                    if item.find('isFullFlag').text == '1':
                        isFull = 'Yes'
                    else:
                        isFull = 'No'

                    q = SeoulBusInfo(
                            bus_id = bus_id,
                            route_id = bus_route,
                            bus_type = bus_type,
                            bus_number = bus_number,
                            gpsX = gpsX,
                            gpsY = gpsY,
                            congestion = congestion,
                            isRunning = isRunning,
                            isFull = isFull
                            )
                    q.save()

            q2 = SeoulBusInfo.objects.filter(route_id=bus_route, isRunning="Yes")
            context = list(q2.values())
            #print(context)
            return JsonResponse(context, safe=False)

        except:
            pass

def get_busan_bus(request):
    if request.method == 'POST':
        url = 'http://apis.data.go.kr/6260000/BusanBIMS/busInfoByRouteId'
        route_id = request.POST['route_id']
        route_name = request.POST['route_name']
        params = '?serviceKey=' + myKey + '&lineid=' + route_id
        request = Request(url + params)
        request.get_method = lambda : 'GET'

        print(route_id)
        print(route_name)
        
        q1 = BusanBusInfo.objects.filter(lineno=route_name)
        for qq in q1:
            qq.isRunning = "No"
            qq.save()

        try:
            response_body = urlopen(request).read()
            root = ET.fromstring(response_body)
            head_code = root.find('./header/resultCode').text
            if head_code == '00':
                total_items = len(root.findall('./body/items/item'))
                for item in root.findall('./body/items/item'):
                    try:
                        carno = item.find('carno').text
                        lineno = item.find('lineno').text
                        bstopnm = item.find('bstopnm').text
                        if item.find('lowplate').text == '0':
                            lowplate = '일반'
                        else:
                            lowplate = '저상'
                        gpsym = item.find('gpsym').text
                        lin = item.find('lin').text
                        lat = item.find('lat').text
                        isRunning = 'Yes'
                        q = BusanBusInfo(
                                carno = carno,
                                lineno = lineno,
                                bstopnm = bstopnm,
                                lowplate = lowplate,
                                gpsym = gpsym,
                                lin = lin,
                                lat = lat,
                                isRunning = isRunning
                                )
                        q.save()

                    except:
                        pass


            print(total_items)
            q2 = BusanBusInfo.objects.filter(lineno=route_name, isRunning='Yes')
            context = list(q2.values())
            #print(context)
            return JsonResponse(context, safe=False)

        except:
            pass

def get_nation_bus(request):
    if request.method == 'POST':
        url = 'http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoBusLcList'
        city_code = request.POST['city_code']
        route_id = request.POST['route_id']
        params = '?serviceKey=' + myKey + '&_type=xml&numOfRows=1000' + '&cityCode=' + city_code + '&routeId=' + route_id
        request = Request(url + params)
        request.get_method = lambda : 'GET'
        print(city_code)
        print(route_id)
        
        q1 = NationBusInfo.objects.filter(routeid=route_id)
        for qq in q1:
            qq.isRunning = "No"
            qq.save()

        try:
            response_body = urlopen(request).read()
            root = ET.fromstring(response_body)
            head_code = root.find('./header/resultCode').text
            if head_code == '00':
                total_items = len(root.findall('./body/items/item'))
                print(total_items)
                for item in root.findall('./body/items/item'):
                    try:
                        vehicleno = item.find('vehicleno').text
                        routenm = item.find('routenm').text
                        routetp = item.find('routetp').text
                        nodenm = item.find('nodenm').text
                        gpslong = item.find('gpslong').text
                        gpslati = item.find('gpslati').text
                        isRunning = 'Yes'
                        q = NationBusInfo(
                                routeid = route_id,
                                vehicleno = vehicleno,
                                routenm = routenm,
                                routetp = routetp,
                                nodenm = nodenm,
                                gpslong = gpslong,
                                gpslati = gpslati,
                                isRunning = isRunning
                                )
                        q.save()

                    except:
                        pass


            q2 = NationBusInfo.objects.filter(routeid=route_id, isRunning='Yes')
            context = list(q2.values())
            return JsonResponse(context, safe=False)

        except:
            pass

def get_seoul_company(request):
    if request.method == 'POST':
        request.encoding = 'utf-8'
        company = request.POST['message']
        print(company)
        q1 = SeoulRouteInfo.objects.filter(company=company)
        context = list(q1.values())
        return JsonResponse(context, safe=False)

    pass

def get_busan_company(request):
    if request.method == 'POST':
        request.encoding = 'utf-8'
        company = request.POST['message']
        print(company)
        q1 = BusanRouteInfo.objects.filter(companyid=company)
        context = list(q1.values())
        return JsonResponse(context, safe=False)

    pass

def get_nation_company(request):
    if request.method == 'POST':
        request.encoding = 'utf-8'
        company = request.POST['message']
        print(company)
        q1 = BusanRouteInfo.objects.filter(companyid=company)
        context = list(q1.values())
        return JsonResponse(context, safe=False)

    pass

def get_seoul_type(type_num):
    result = "공융"

    if type_num == 1:
        result = "공항"
    elif type_num == 2:
        result = "마을"
    elif type_num == 3:
        result = "간선"
    elif type_num == 4:
        result = "지선"
    elif type_num == 5:
        result = "순환"
    elif type_num == 6:
        result = "광역"
    elif type_num == 7:
        result = "인천"
    elif type_num == 8:
        result = "경기"
    elif type_num == 9:
        result = "폐지"

    return result

def getCongestion(value):
    result = '없음'

    if value == 3:
        result = '여유'
    if value == 4:
        result = '보통'
    if value == 5:
        result = '혼잡'
    if value == 6:
        result = '매우혼잡'

    return result
