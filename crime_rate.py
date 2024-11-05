# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 15:46:41 2022

@author: zq
"""

import pandas as pd
import datetime as dt

df = pd.read_csv('1797ead8-8262-41cc-9099-cbc8a161924b.csv')
df['INCIDENTTIME'] = pd.to_datetime(df['INCIDENTTIME'])
df['INCIDENTDATE'] = df['INCIDENTTIME'].dt.date
df['INCIDENTHOUR'] = df['INCIDENTTIME'].dt.hour
df = df[['INCIDENTDATE', 'INCIDENTHOUR', 'INCIDENTLOCATION', 'INCIDENTNEIGHBORHOOD', 'INCIDENTHIERARCHYDESC', 'OFFENSES', 'X', 'Y']]
df.to_csv('CRIME_RATE.csv', index=False)