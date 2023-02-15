from django.shortcuts import render
from django.shortcuts import render
from .models import Emissions, Countries
from django.http import JsonResponse
from json import dumps
from plotly.offline import plot
import plotly.graph_objs as go
from django.db.models import Max, Sum

def emissions(request):
    max_pop = maxPopulation(request)
    max_co2_dict = maxCO2(request)
    max_co2_per_capita_dict = maxCO2_per_capita(request)
    max_co2_cum = maxCumulative_CO2(request)
    emissions_per_capita_dict = emissionPerCapita(request)
    dict_sorted_emissions = sortDictionary(emissions_per_capita_dict)
    plot_bar = barPlot()
    plot_bubble = bubblePlot()
    wfc = waterfallChart()
    top_polluters_bySource = topCO2BySource()
    return render(request, "emissions.html",{"max_pop":max_pop, "max_co2":max_co2_dict,
    "max_co2_capita": max_co2_per_capita_dict, "max_cum": max_co2_cum,
    "epcd":dumps(emissions_per_capita_dict), "top7":dict_sorted_emissions,
    "plot_bar":plot_bar, "plot_bubble": plot_bubble, "wfc": wfc, 
    "tpbs":top_polluters_bySource})

# Get Country with max population, return as a dictionary
def maxPopulation(request):
    
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
    tuple_result = max(zip(dict_population.values(), dict_population.keys()))
    dict_result = {}
    dict_result['pop'] = tuple_result[0]
    dict_result['country'] = tuple_result[1]
    return dict_result

#Maximum CO2 output
def maxCO2(request):
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
    tuple_result = max(zip(dict_co2.values(), dict_co2.keys()))
    dict_result = {}
    dict_result['co2'] = tuple_result[0]
    dict_result['country'] = tuple_result[1]
    return dict_result

def maxCO2_per_capita(request):
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
    tuple_result = max(zip(dict_co2.values(), dict_co2.keys()))
    dict_result = {}
    dict_result['co2'] = tuple_result[0]
    dict_result['country'] = tuple_result[1]
    return dict_result

def maxCumulative_CO2(request):
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
    tuple_result = max(zip(dict_co2.values(), dict_co2.keys()))
    dict_result = {}
    dict_result['co2'] = tuple_result[0]
    dict_result['country'] = tuple_result[1]
    return dict_result

#Getting data for world-map
def emissionPerCapita(request):
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

    return dict_result

def sortDictionary(dict_v, intTopX=7):
    sorted_dict = dict(sorted(dict_v.items(),key=lambda x:x[1], reverse=True))
    dataset_iso = Countries.objects.values('alpha_2', 'country')
    dict_iso = {}
    for l in list(dataset_iso):
        dict_iso[l['alpha_2']] = l['country']

    count = 0
    dict_result = {}
    for index, value in sorted_dict.items():
        dict_result[dict_iso[index]]  = round(value,3)
        count += 1
        if count > intTopX-1:
            break

    return dict_result

def barPlot():
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries']
    filter_year = '2020'
    x_axis = []
    y_pop = []
    y_co2 = []
    dataset = Emissions.objects.values('country', 'year', 'population', 'co2')
    for d in dataset:
        if d['country'] in filter_list and d['year'] == filter_year:
            x_axis.append(d['country'])
            y_pop.append(int(d['population']))
            y_co2.append(float(d['co2']))

    #plot the graph
    fig = go.Figure(
    data=[
        go.Bar(name='Population', x=x_axis, y=y_pop, yaxis='y', offsetgroup=1),
        go.Bar(name='CO2 Emissions', x=x_axis, y=y_co2, yaxis='y2', offsetgroup=2)
    ],
    layout={
        'yaxis': {'title': 'Population'},
        'yaxis2': {'title': 'CO2 Emissions', 'overlaying': 'y', 'side': 'right'},
    }
    )
 
    # Change the bar mode
    fig.update_layout(barmode='group')
    
    plt_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plt_div

def bubblePlot():
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries', 'World',
    'Asia', 'Africa', 'Europe', 'North America', 'South America', 'European Union (27)', 
    'Oceania', 'European Union (28)', 'Asia (excl. China & India)', 'Europe (excl. EU-27)',
    'Europe (excl. EU-28)', 'International transport','Kuwaiti Oil Fires', 'Panama Canal Zone',
    'North America (excl. USA)']

    data_set = Emissions.objects.values('country', 'year', 'co2', 'population', 'gdp')
    data_set = data_set.filter(year='2018')
    data_set = data_set.exclude(country__in=filter_list)
    x_axis = []
    y_axis = []
    text_co2 = []
    bubble_size = []
    for d in data_set:
        try:
            x_axis.append(float(d['gdp']))
        except:
            x_axis.append(0)
        try:
            y_axis.append(float(d['population']))
        except:
            y_axis.append(0)

        text_co2.append(d['country'] + ': <br> CO2:' + str(d['co2']))
        
        try:
            bubble_size.append(float(d['co2']))
        except:
            bubble_size.append(0)

    new_layout = go.Layout(
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0, #top margin
        ))
    fig = go.Figure(layout=new_layout, data=[go.Scatter(
        x = x_axis, y = y_axis, text=text_co2, mode='markers',
        marker=dict(
            size=bubble_size,
            sizemode='area',
            sizeref = 2.*max(bubble_size)/(2000),
            sizemin=4
        )
    )])

    fig.update_layout(
    xaxis_title="GDP (2018 dollars)",
    yaxis_title="Population",
    legend_title="Legend Title",
    font=dict(
        size=10,
        color="RebeccaPurple"
        )
    )

    plt_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plt_div

def waterfallChart():
    elements_interest_list = ['cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2',
    'oil_co2', 'other_industry_co2']
    filter_list = ['World']

    filter_year = '2020'
    data_set = Emissions.objects.values('country', 'co2', 'cement_co2', 'coal_co2', 'flaring_co2',
    'gas_co2', 'oil_co2', 'other_industry_co2')
    data_set = data_set.filter(year=filter_year)
    data_set = data_set.filter(country__in=filter_list)
    measure = []
    y = []
    for d in elements_interest_list:
        measure.append("relative")
        y.append(float(data_set[0][d]))
    y.append(0)
    measure.append("total")

    elements_interest_list.append("Total")

    new_layout = go.Layout(
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0, #top margin
        ))

    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = measure,
        x = elements_interest_list,
        textposition = "outside",
        y = y,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ), layout=new_layout)
    

    plt_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plt_div

def topCO2BySource():
    filter_list = ['High-income countries', 'Low-income countries',
    'Lower-middle-income countries', 'Upper-middle-income countries', 'World',
    'Asia', 'Africa', 'Europe', 'North America', 'South America', 'European Union (27)', 
    'Oceania', 'European Union (28)', 'Asia (excl. China & India)', 'Europe (excl. EU-27)',
    'Europe (excl. EU-28)', 'International transport','Kuwaiti Oil Fires', 'Panama Canal Zone',
    'North America (excl. USA)']
    filter_year = '2020'
    data_set = Emissions.objects.values('country', 'co2', 'cement_co2', 'coal_co2', 'flaring_co2',
    'gas_co2', 'oil_co2', 'other_industry_co2')

    lst_sources = ['cement_co2', 'coal_co2', 'flaring_co2',
    'gas_co2', 'oil_co2', 'other_industry_co2']
    dict_max = {'cement_co2':0, 'coal_co2':0, 'flaring_co2':0, 'gas_co2': 0, 'oil_co2':0,
    'other_industry_co2':0}
    dict_sum = {'cement_co2':0, 'coal_co2':0, 'flaring_co2':0, 'gas_co2': 0, 'oil_co2':0,
    'other_industry_co2':0}
    dict_country = {'cement_co2':"N/A", 'coal_co2':"N/A", 'flaring_co2':"N/A", 
    'gas_co2': "N/A", 'oil_co2':"N/A",'other_industry_co2':"N/A"}
    dict_result = {'cement_co2':["N/A",0], 'coal_co2':["N/A",0], 'flaring_co2':["N/A",0], 
    'gas_co2': ["N/A",0], 'oil_co2':["N/A",0],'other_industry_co2':["N/A",0]}

    data_set = data_set.filter(year=filter_year)
    data_set = data_set.exclude(country__in=filter_list)

    for d in data_set:
        for l in lst_sources:
            temp_val = 0
            try:
                temp_val = float(d[l])
            except:
                temp_val = 0
            if temp_val > dict_max[l]:
                dict_max[l] = temp_val
                dict_country[l] = d['country']
            dict_sum[l] = dict_sum[l] + temp_val

    for l in lst_sources:
        temp_lst = []
        temp_lst.append(dict_country[l])
        percentage = int((dict_max[l]/dict_sum[l])*100)
        temp_lst.append(percentage)
        dict_result[l] = temp_lst

    return dict_result
 
# Create your views here.
