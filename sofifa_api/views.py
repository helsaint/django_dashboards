from django.shortcuts import render
from .models import Sofifa
from .serializers import GeneralSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import pandas as pd
from plotly.offline import plot
import datetime
import plotly.express as px

def sofifa_general_api_default(request):
    return render(request, 'sofifa_general_api.html',{})

@api_view(['GET'])
def choroplethData(request):
    queryset = Sofifa.objects.values_list('player_id', 'nationality_name')
    df = pd.DataFrame(list(queryset), columns=['player_id', 'nationality_name'])
    df_cc = pd.read_csv('./csvs/country_code.csv')
    df1 = pd.pivot_table(df, index='nationality_name',
                         values=['player_id'],
                         aggfunc='count')
    dict_result = {}
    df1 = df1.reset_index()
    df1['nationality_name'] = df1['nationality_name'].str.strip()
    uk_sum = df1[(df1['nationality_name'] == 'Scotland') | (df1['nationality_name'] == 'England')|
              (df1['nationality_name'] == 'Wales') | 
              (df1['nationality_name'] == 'Northern Ireland')]['player_id'].sum()
    df_uk = pd.DataFrame([['United Kingdom', uk_sum]], columns=['nationality_name','player_id'])
    df1 = pd.concat([df1, df_uk])
    df2 = pd.merge(df1,df_cc, left_on=['nationality_name'], right_on=['name'],
                   how='left')
    df2 = df2[df2['code'].notna()]
    
    dict_result = dict(zip(list(df2['code']), list(df2['player_id'])))
    return JsonResponse(dict_result, safe=False)

@api_view(['GET'])
def bubblePlotEarning(request):
    queryset = Sofifa.objects.values_list('short_name', 'overall', 'wage_eur', 'value_eur')
    df = pd.DataFrame(list(queryset),
                      columns=['short_name', 'overall', 'wage_eur', 'value_eur'])
    dict_result = {}
    dict_result['short_name'] = list(df['short_name'])
    dict_result['overall'] = list(df['overall'])
    dict_result['wage_eur'] = list(df['wage_eur'])
    dict_result['value_eur'] = list(df['value_eur']) 
    return JsonResponse(dict_result, safe=False)

@api_view(['GET'])
def generalPlayerStats(request):
    dict_result_test = {'test1':80, 'test2':20}
    dict_result = {}
    queryset = Sofifa.objects.values_list('player_id', 'short_name', 'overall', 'age', 'value_eur',
                                     'wage_eur','height_cm', 'weight_kg', 'league_name', 'club_name',
                                     'club_position', 'nationality_name', 'player_face_url')
    
    df = pd.DataFrame(list(queryset),
                      columns=['player_id', 'short_name', 'overall', 'age', 'value_eur',
                               'wage_eur','height_cm', 'weight_kg', 'league_name', 'club_name',
                               'club_position', 'nationality_name', 'player_face_url'])
    dict_result['Player Count'] = len(df['player_id'].unique())
    dict_result['Median Age'] = df['age'].median()
    df['wage_eur'] = df['wage_eur'].str.replace('$', '')
    df['wage_eur'] = df['wage_eur'].str.replace(',', '')
    df['wage_eur'] = df['wage_eur'].astype(float)
    df['value_eur'] = df['value_eur'].str.replace('$', '')
    df['value_eur'] = df['value_eur'].str.replace(',', '')
    df['value_eur'] = df['value_eur'].astype(float)
    dict_result['Median Wage'] =  '\u20AC'+"{:,.0f}".format(df['wage_eur'].median())
    dict_result['Median Height'] = "{:,.0f}".format(df['height_cm'].median()) +"cm"
    dict_result['Median Weight'] = str(df['weight_kg'].median())+"kg"
    dict_result['Mode Nationality'] = df['nationality_name'].mode()[0]
    df2 = pd.pivot_table(df, index=['league_name'], values=['wage_eur'], aggfunc=pd.Series.sum,
                         fill_value=0)
    df2.reset_index(inplace=True)
    str_richest_league = df2.sort_values(by=['wage_eur']).iloc[-1]['league_name']
    dict_result['Best Paying League'] = str_richest_league
    df2 = df[(df['league_name'] == str_richest_league)]
    dict_result['Median Wage in ' + str_richest_league] = '\u20AC'+"{:,.0f}".format(df2['wage_eur'].median())
    df2 = pd.pivot_table(df, index=['league_name'], values=['value_eur'],
                         aggfunc=pd.Series.sum, fill_value=0)
    df2.reset_index(inplace=True)
    str_mv_league = df2.sort_values(by=['value_eur']).iloc[-1]['league_name']
    dict_result['Most Valuable League'] = str_mv_league
    df2 = df[(df['league_name'] == str_mv_league)]
    dict_result['Median Value in ' + str_mv_league] = '\u20AC'+"{:,.0f}".format(df2['value_eur'].median())
    str_mvp_name = df[df['value_eur']==df['value_eur'].max()]['short_name'].item()
    dict_result['Most Valuable Player'] = str_mvp_name
    dict_result[str_mvp_name + ' Value'] = '\u20AC'+"{:,.0f}".format(df[df['value_eur']==df['value_eur'].max()]['value_eur'].item()/1000000)+"MM"
    
    return JsonResponse(dict_result,safe=False)

def player_detail(request, name):
    player_data = Sofifa.objects.filter(short_name=name).values()
    data_final = []
    for key, value in player_data[0].items():
        temp_dict = {}
        temp_dict['feature'] = str(key)
        temp_dict['value'] = str(value)
        data_final.append(temp_dict)

    # Spider Chart takes the queryset data and list of 
    # features of interest
    lst_sc_points = ['pace', 'shooting', 'passing', 'dribbling',
                      'defending', 'physic']
    px_general = spider_chart(player_data, lst_sc_points, 
                              title="Spider web of " + name + " general prowess")
    lst_sc_points = ['attacking_crossing',
                      'attacking_finishing', 'attacking_heading_accuracy',
                      'attacking_short_passing', 'attacking_volleys']
    px_attacking = spider_chart(player_data, lst_sc_points,
                                title="Spider web of " + name + " attacking prowess")
    
    
    return render(request, 'player_info.html', {'player_data': data_final, 
                                                'px_general': px_general,
                                                'px_attacking': px_attacking, 
                                                'player_name': name})
    
def country_detail(request, name):
    df_cc = pd.read_csv('./csvs/country_code.csv')
    country = [df_cc[df_cc['code'] == name]['name'].iloc[0]]
    today = datetime.date.today()
    year = today.year

    if (country[0] == 'United Kingdom'):
        country = ['England', 'Scotland', 'Wales', 'Northern Ireland']
    data_final = []
    for c in country:
        country_data = Sofifa.objects.filter(nationality_name=c, 
                                             club_contract_valid_until_year__gte=year).values(
                                                                        'short_name',
                                                                        'long_name', 'age',
                                                                        'value_eur', 'wage_eur', 
                                                                        'club_name', 'league_name', 
                                                                        'league_level',
                                                                        'overall','player_traits',
                                                                        'club_contract_valid_until_year')
        data_final.extend(list(country_data))
    for d in data_final:
        if (d['value_eur'] is None):
            d['value_eur'] = '0.00'
        if (',' in d['value_eur']):
            d['value_eur'] = d['value_eur'].replace(',', '')
        d['value_eur'] = d['value_eur'].replace('$', '')
        d['value_eur'] = float(d['value_eur'])
    
    for d in data_final:
        if (d['wage_eur'] is None):
            d['wage_eur'] = '0.00'
        if (',' in d['wage_eur']):
            d['wage_eur'] = d['wage_eur'].replace(',', '')
        d['wage_eur'] = d['wage_eur'].replace('$', '')
        d['wage_eur'] = float(d['wage_eur'])

    data_final = sorted(data_final, key=lambda x:x['value_eur'], reverse=True)
    for  d in data_final:
        d['value_eur'] = '€{:,.2f}'.format(d['value_eur'])
        d['wage_eur'] = '€{:,.2f}'.format(d['wage_eur'])
    
    return render(request, 'country_detail.html', {'country_data': data_final})

#General code to add a plotly plot to html. below uses plotly.express
    #x_data = [0,1,2,3,4,5]
    #y_data = [x**2 for x in x_data]
    #fig = px.scatter(x=x_data, y=y_data)
    #px_div = plot(fig, output_type='div')
def spider_chart(dataset, lst_points,title="Spider web data"):
    temp_dict = dataset[0]
    theta = lst_points
    r = [temp_dict.get(k) for k in theta]
    sort_index = np.argsort(np.array(r))
    r_sort = [r[i] for i in sort_index]
    theta_sort = [theta[i] for i in sort_index]

    fig = go.Figure(data=go.Scatterpolar(
        r=r_sort,
        theta=theta_sort,
        fill='toself',
        marker = dict(color = 'rgb(35, 193, 134)'),
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True),),
        showlegend=False,
        title=title,
    )
    return(plot(fig, output_type='div'))


class GeneralAllView(generics.ListAPIView):
    queryset = Sofifa.objects.values('player_id', 'short_name', 'overall', 'age', 'value_eur',
                                     'wage_eur','height_cm', 'weight_kg', 'league_name', 'club_name',
                                     'club_position', 'nationality_name', 'player_face_url')
    serializer_class = GeneralSerializer



# Create your views here.


# Create your views here.
