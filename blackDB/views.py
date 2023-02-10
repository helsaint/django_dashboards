from django.shortcuts import render
from .models import Emissions, Countries
from django.http import JsonResponse
from json import dumps

# Create your views here.

def blackdb_return(request):
    return render(request, 'blackdb.html',{})

def blackdb_chart_data(request):
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries']
    filter_year = '2020'
    dataset = Emissions.objects.values('country', 'year', 'population', 'co2')
    dict_population = dict()
    for d in dataset:
        if d['country'] in filter_list and d['year'] == filter_year:
            dict_population[d['country']] = (d['population'], d['co2'])
    
    data = dumps(dict_population)
    return JsonResponse(data,safe=False)

def max_population(request):
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries', 'World',
    'Asia', 'Africa', 'Europe', 'North America', 'South America', 'European Union (27)']

    data_pop = Emissions.objects.values('country', 'year', 'population')
    data_pop = data_pop.filter(year='2020')
    data_pop = data_pop.exclude(country__in=filter_list)
    lst_country = []
    lst_population = []
    for d in data_pop:
        lst_country.append(d['country'])
        try:
            lst_population.append(int(d['population']))
        except:
            lst_population.append(0)
    dict_population= dict(zip(lst_country,lst_population))
    dict_result = max(zip(dict_population.values(), dict_population.keys()))
    data = dumps(dict_result)
    return JsonResponse(data, safe=False)

def max_co2(request):
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries', 'World',
    'Asia', 'Africa', 'Europe', 'North America', 'South America', 'European Union (27)']
    data = Emissions.objects.values('country', 'year', 'co2')
    data = data.filter(year='2020')
    data = data.exclude(country__in=filter_list)
    lst_country = []
    lst_co2 = []
    for d in data:
        lst_country.append(d['country'])
        try:
            lst_co2.append(float(d['co2']))
        except:
            lst_co2.append(0)
    dict_co2 = dict(zip(lst_country,lst_co2))
    dict_result = max(zip(dict_co2.values(), dict_co2.keys()))
    data = dumps(dict_result)
    return JsonResponse(data, safe=False)

def max_co2_per_capita(request):
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries', 'World',
    'Asia', 'Africa', 'Europe', 'North America', 'South America', 'European Union (27)']
    data = Emissions.objects.values('country', 'year', 'co2_per_capita')
    data = data.filter(year='2020')
    data = data.exclude(country__in=filter_list)
    lst_country = []
    lst_co2 = []
    for d in data:
        lst_country.append(d['country'])
        try:
            lst_co2.append(float(d['co2_per_capita']))
        except:
            lst_co2.append(0)
    dict_co2 = dict(zip(lst_country,lst_co2))
    dict_result = max(zip(dict_co2.values(), dict_co2.keys()))
    data = dumps(dict_result)
    return JsonResponse(data, safe=False)

def max_cumulative_co2(request):
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries', 'World',
    'Asia', 'Africa', 'Europe', 'North America', 'South America', 'European Union (27)']
    data = Emissions.objects.values('country', 'year', 'cumulative_co2')
    data = data.filter(year='2020')
    data = data.exclude(country__in=filter_list)
    lst_country = []
    lst_co2 = []
    for d in data:
        lst_country.append(d['country'])
        try:
            lst_co2.append(float(d['cumulative_co2']))
        except:
            lst_co2.append(0)
    dict_co2 = dict(zip(lst_country,lst_co2))
    dict_result = max(zip(dict_co2.values(), dict_co2.keys()))
    data = dumps(dict_result)
    return JsonResponse(data, safe=False)

def emissions_per_capita(request):
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries', 'World',
    'Asia', 'Africa', 'Europe', 'North America', 'South America', 'European Union (27)']

    #Only columns of interest are pulled, because no primary key was created in the
    #When the SQLITE db was created if we try Emissions.objects.all() we'll get an error
    #Stating that Emissions._id column doesn't exis. For some reason Django auto creates this
    #Column in the python manage.py makemigrations x
    data = Emissions.objects.values('country', 'year', 'co2', 'iso_code', 'population')
    dataset_iso = Countries.objects.values('alpha_3', 'alpha_2')
    dict_iso = {}
    #The map in javascript uses 2 character ISO format while our data uses a 3 character format
    #This dictionary will convert the 3 formatted codes to 2 later on. In the meanwhile, we
    #Keep it as a dictionary
    for l in list(dataset_iso):
        dict_iso[l['alpha_3']] = l['alpha_2']

    #We are only interested in data from 2020 and only want individual countries not groupings.
    data = data.filter(year='2020')
    data = data.exclude(country__in=filter_list)
    dict_result = {}
    for l in list(data):
        if l['iso_code'] in dict_iso.keys():
            fPop = 0.0
            fCO2 = 0.0
            try:
                fPop = float(l['population'])
                fCO2 = float(l['co2'])
                dict_result[dict_iso[l['iso_code']]] = (fCO2/fPop)*1000000
            except:
                dict_result[dict_iso[l['iso_code']]] = 0.0

    result = dumps(dict_result)
    return JsonResponse(result, safe=False)
