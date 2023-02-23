import requests
import pandas as pd
from pandas import json_normalize
import numpy as np
import datetime
import plotly.graph_objects as go

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

def vindrose12(datetime_start, datetime_end, idnr, api_key, data_type,file_direction,months):
    datetimes = datetime_start + '/' + datetime_end
    start_date = datetime.datetime.strptime(datetime_start, '%Y-%m-%dT%H:%M:%SZ')
    end_date = datetime.datetime.strptime(datetime_end, '%Y-%m-%dT%H:%M:%SZ')
    start_date = start_date.strftime('%d-%m-%Y')
    end_date = end_date.strftime('%d-%m-%Y')
    ######################################

    if data_type == 'stationValue':
        data_geo_res = 'stationId='
    elif data_type == '10kmGridValue' or data_type == '20kmGridValue':
        data_geo_res = 'cellId='
    elif data_type == 'municipalityValue':
        data_geo_res = 'municipalityId='

    # Can't get data from anything but climateData
    base_url = 'https://dmigw.govcloud.dk/v2/climateData/collections/'

    #####

    url = base_url + data_type + '/items?api-key=' + api_key + '&datetime=' + datetimes + '&' + data_geo_res + idnr + '&timeResolution=hour&'
    wind_url = url + 'parameterId=mean_wind_speed&limit=300000'
    wind_dir_url = url + 'parameterId=mean_wind_dir&limit=300000'

    r_dir = requests.get(wind_dir_url)
    r_wind = requests.get(wind_url)
    print(r_dir, r_wind)
    print(wind_url)
    json_dir = r_dir.json()
    json_wind = r_wind.json()



    df_wind = json_normalize(json_wind['features'])
    df_wind = df_wind[['properties.from','properties.to','properties.value']]
    df_dir = json_normalize(json_dir['features'])
    df_dir = df_dir[['properties.from','properties.to','properties.value']]
    df_dir.rename(columns = {'properties.value':'direction'}, inplace = True)
    df_wind.rename(columns = {'properties.value':'Vindhastighed'}, inplace = True)

    vindrose = pd.merge(df_dir, df_wind, on=['properties.from','properties.to'])
    retning = []
    retning1 = []

    conditions = [
        (vindrose['direction'] <= 15),
        (vindrose['direction'] > 15) & (vindrose['direction'] <=45),
        (vindrose['direction'] > 45) & (vindrose['direction'] <=75),
        (vindrose['direction'] > 75) & (vindrose['direction'] <=105),
        (vindrose['direction'] > 105) & (vindrose['direction'] <=135),
        (vindrose['direction'] > 135) & (vindrose['direction'] <=165),
        (vindrose['direction'] > 165) & (vindrose['direction'] <=195),
        (vindrose['direction'] > 195) & (vindrose['direction'] <=225),
        (vindrose['direction'] > 225) & (vindrose['direction'] <=255),
        (vindrose['direction'] > 255) & (vindrose['direction'] <=285),
        (vindrose['direction'] > 285) & (vindrose['direction'] <=315),
        (vindrose['direction'] > 315) & (vindrose['direction'] <=345),
        (vindrose['direction'] > 345) & (vindrose['direction'] <=360),
        ]
    value_degree = [360,30,60,90,120,150,180,210,240,270,300,330,360]
    values_corner = ['N','NE','EN','E','ES','SE','S','SW','WS','W','WN','NW','N']

    vindrose['Retning2'] = np.select(conditions, value_degree)
    vindrose['degrees_corners'] = np.select(conditions, values_corner)
    vindrose['Retning2'].astype(float)
    vindrose['Vindhastighed'].astype(float)
    over11 = [(len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==360)])) / sum(vindrose['Retning2'].value_counts()) * 100,
              (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==30)])) / sum(vindrose['Retning2'].value_counts()) * 100,
              (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==60)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==90)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==120)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==150)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==180)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==210)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==240)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==270)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==300)])) / sum(vindrose['Retning2'].value_counts()) * 100,
             (len(vindrose.loc[(vindrose['Vindhastighed'] >= 11) &  (vindrose['Retning2']==330)])) / sum(vindrose['Retning2'].value_counts()) * 100]

    m8og11 = [len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==360)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==30)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==60)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==90)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==120)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==150)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==180)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==210)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==240)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==270)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==300)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 11) & (vindrose['Vindhastighed'] >= 8) & (vindrose['Retning2']==330)]) / sum(vindrose['Retning2'].value_counts()) * 100]

    m6og8 = [len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==360)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==30)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==60)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==90)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==120)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==150)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==180)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==210)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==240)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==270)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==300)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 8) & (vindrose['Vindhastighed'] >= 6) & (vindrose['Retning2']==330)]) / sum(vindrose['Retning2'].value_counts()) * 100]

    m4og6 = [len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==360)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==30)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==60)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==90)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==120)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==150)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==180)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==210)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==240)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==270)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==300)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 6) & (vindrose['Vindhastighed'] >= 4) & (vindrose['Retning2']==330)]) / sum(vindrose['Retning2'].value_counts()) * 100]


    m0og4 = [len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==360)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==30)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==60)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==90)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==120)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==150)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==180)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==210)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==240)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==270)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==300)]) / sum(vindrose['Retning2'].value_counts()) * 100,
              len(vindrose.loc[(vindrose['Vindhastighed'] < 4) & (vindrose['Vindhastighed'] > 0) & (vindrose['Retning2']==330)]) / sum(vindrose['Retning2'].value_counts()) * 100]

    # Get name of station

    url3 = 'https://dmigw.govcloud.dk/v2/climateData/collections/station/items'
    params3 = {'api-key': api_key,
             'limit': '1000'}
    r2 = requests.get(url3, params=params3)
    print(r2)
    json = r2.json()

    for x in json['features']:
        if x['properties']['stationId'] == idnr:
            rnavn = x['properties']['name']
    if data_type == 'municipalityValue':
        rnavn = 'Københavns Kommune'

    # Plot station
    fig = go.Figure()
    fig.add_trace(go.Barpolar(
        r=m0og4,
        name='<4.0m/s',
        marker_color='rgb(0,255,0)',
        width=30,
        marker=dict(
            line=dict(
                color="black")

        )))
    fig.add_trace(go.Barpolar(
        r=m4og6,
        name='4.0-5.9m/s',
        marker_color='rgb(255,255,0)',
        width=30,
        marker=dict(
            line=dict(
                color="black")
        )))

    fig.add_trace(go.Barpolar(
        r=m6og8,
        name='6.0-7.9m/s',
        marker_color='rgb(153,51,0)',
        width=30,
        marker=dict(
            line=dict(
                color="black")
        )))

    fig.add_trace(go.Barpolar(
        r=m8og11,
        name='8.0-10.9m/s',
        marker_color='rgb(255,0,0)',
        width=30,
        marker=dict(
            line=dict(
                color="black")

        )))

    fig.add_trace(go.Barpolar(
        r=over11,
        name='>=11.0m/s',
        marker_color='rgb(255,151,151)',
        width=30,
        marker=dict(
            line=dict(
                color="black")

        )))

    # fig.update_traces(text=['N', '30', '60', 'E', '120', '150', 'S', '210', '240', 'W', '300', '330'])


    fig.add_annotation(
        text=rnavn,
        xref="paper",
        yref="paper",
        x=0.5,
        y=1.16,
        showarrow=False,
        font=dict(
            family="Times New Roman",
            size=20,
            color="black")),
    fig.add_annotation(
        text=str(start_date) + " til " + str(end_date),
        xref="paper",
        yref="paper",
        x=0.5,
        y=1.1,
        showarrow=False,
        font=dict(
            family="Times New Roman",
            size=10,
            color="black")),
    fig.add_annotation(
        text="Station " + idnr,
        xref="paper",
        yref="paper",
        x=0.5,
        y=1.18,
        showarrow=False,
        font=dict(
            family="Times New Roman",
            size=10,
            color="black")),

    fig.update_layout(
        legend=dict(
            xanchor="left",
            x=0.66,
            yanchor="bottom",
            y=0),
        legend_title="Percent:",
        font=dict(
            family="Times New Roman",
            size=8,
            color="black"),
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                showticklabels=True,
                tickfont_size=14,
                tickfont_color="black",
                tickmode="array",
                tickvals=[5, 10, 15, 20, 25, 30, 35, 40],
                ticktext=['5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%'],
                gridcolor="black",
                showgrid=True,
                # angle=270,
                showline=False,
                gridwidth=0.1,
                tickangle=360,
                layer="above traces"
            ),
            angularaxis=dict(
                tickfont_size=10,
                rotation=90,
                linewidth=1,
                showline=True,
                linecolor="black",
                gridcolor="black",
                showgrid=True,
                tickmode="array",
                tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
                ticktext=['N', '30', '60', 'E', '120', '150', 'S', '210', '240', 'W', '300', '330'],
                direction="clockwise"
            ),
        ))
    if months != 'yes':
        fig.show()
    fig.write_image(file_direction + '\Vindrose {} - {}.jpeg'.format(start_date, end_date))
    print(np.round(m0og4, decimals=2))
    print(np.round(m4og6, decimals=2))
    print(np.round(m6og8, decimals=2))
    print(np.round(m8og11, decimals=2))
    print(np.round(over11, decimals=2))
    print(np.round(sum(m0og4), decimals=2), np.round(sum(m4og6), decimals=2), \
          np.round(sum(m6og8), decimals=2), np.round(sum(m8og11), decimals=2), \
          np.round(sum(over11), decimals=2))
    print(np.round(vindrose.head(), decimals=2))
    print(sum(m0og4) + sum(m4og6) + sum(m6og8) + sum(m8og11) + sum(over11))