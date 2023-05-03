from django.shortcuts import render
from .models import Sofifa
from .serializers import GeneralSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import pandas as pd
from plotly.offline import plot
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


class GeneralAllView(generics.ListAPIView):
    queryset = Sofifa.objects.values('player_id', 'short_name', 'overall', 'age', 'value_eur',
                                     'wage_eur','height_cm', 'weight_kg', 'league_name', 'club_name',
                                     'club_position', 'nationality_name', 'player_face_url')
    serializer_class = GeneralSerializer



# Create your views here.


# Create your views here.
