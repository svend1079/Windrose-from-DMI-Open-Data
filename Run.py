import requests
import pandas as pd
from pandas import json_normalize
import numpy as np
import datetime
import plotly.graph_objects as go
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from Vindrose12 import vindrose12
from Vindrose8 import vindrose8
from Vindrose16 import vindrose16

# Write either stationValue, 10kmGridValue, 20kmGridValue or municipalityValue
data_type = 'stationValue'
# Write the id for the cell, station or municipality
# Station example: 06188. 10km example: 10km_634_61. 20km example: 20km_628_65. Munic: 0101.
idnr = '06180'
# Write API key for DMI Open Data
api_key = '3d060a77-29be-41ef-8b31-2c74dce37dbe'
#Write the datetime
# Format: 2022-01-01T00:00:00Z
datetime_start = '2012-01-01T00:00:00Z'
datetime_end = '2012-04-01T00:00:00Z'
start_date = datetime.datetime.strptime(datetime_start, '%Y-%m-%dT%H:%M:%SZ')
end_date = datetime.datetime.strptime(datetime_end, '%Y-%m-%dT%H:%M:%SZ')
# Choose which windrose you want. 8, 12 or 16 directions.
windrose_type = '8'
# If you want pr. month, write 'yes', otherwise write anything else.
months = 'no'

# Write the directory of where the images should be saved
# NOTE: Do NOT delete the 'r'
file_direction = r'C:\Users\svend\OneDrive - University of Copenhagen\Desktop\16'

if windrose_type == '8':
    vindrose8(datetime_start,datetime_end,idnr,api_key,data_type,file_direction,months)
elif windrose_type == '12':
    vindrose12(datetime_start,datetime_end,idnr,api_key,data_type,file_direction,months)
elif windrose_type == '16':
    vindrose16(datetime_start,datetime_end,idnr,api_key,data_type,file_direction,months)

if months == 'yes':
    if windrose_type == '8':
        for dt_start in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            start_dt_months = dt_start
            end_dt_months = dt_start + relativedelta(months=1)
            dt_start_month_Z = start_dt_months.strftime('%Y-%m-%dT%H:%M:%SZ')
            dt_end_month_Z = end_dt_months.strftime('%Y-%m-%dT%H:%M:%SZ')
            vindrose8(dt_start_month_Z,dt_end_month_Z,idnr,api_key,data_type,file_direction,months)
    elif windrose_type == '12':
        for dt_start in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            start_dt_months = dt_start
            end_dt_months = dt_start + relativedelta(months=1)
            dt_start_month_Z = start_dt_months.strftime('%Y-%m-%dT%H:%M:%SZ')
            dt_end_month_Z = end_dt_months.strftime('%Y-%m-%dT%H:%M:%SZ')
            vindrose12(dt_start_month_Z, dt_end_month_Z, idnr, api_key, data_type,file_direction,months)
    elif windrose_type == '16':
        for dt_start in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            start_dt_months = dt_start
            end_dt_months = dt_start + relativedelta(months=1)
            dt_start_month_Z = start_dt_months.strftime('%Y-%m-%dT%H:%M:%SZ')
            dt_end_month_Z = end_dt_months.strftime('%Y-%m-%dT%H:%M:%SZ')
            vindrose16(dt_start_month_Z, dt_end_month_Z, idnr, api_key, data_type,file_direction,months)