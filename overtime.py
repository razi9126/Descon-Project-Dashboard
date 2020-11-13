# The program makes a dictionary with months as keys, and the values are top 5 crafts clocking in the most hours as overtime hours
import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import collections
import pandas as pd
from colour import Color
from datetime import datetime
from textwrap import dedent as d
import json
import re
import pickle

def percentage(row):
    ## Place 0's where Nan so that we can add the values
    row = row.fillna(0)   
    ## Rounding the results to 2 decimal places
    return round((sum(row[2:])/sum(row[1:])*100),1)


# Read the data file
ot = pd.read_excel("./Craftwise_Overtime.xlsx")
ot.iloc[2:,0:2] = ot.iloc[2:,0:2].ffill()
# display(ot.iloc[2:,0:2])
## Filtering employees with Indirect or Not assigned type
indirect = ot[(ot['Calendar Year/Month'] =='Time Type')|(ot['Calendar Year/Month'] =='Direct/Indirect Type')|(ot['Calendar Year/Month'] =='I') |(ot['Calendar Year/Month'] =='Not assigned')]
## Filtering employees with Direct type
direct = ot[(ot['Calendar Year/Month'] =='Time Type')|(ot['Calendar Year/Month'] =='Direct/Indirect Type')|(ot['Calendar Year/Month'] =='D')]

dict = {}


cols = []
start = 1
for i in indirect.iloc[:, 3:].columns:
    if start:
        cols.append('Unnamed: 1')
        cols.append(i)
        start = 0
    else:
        if len(i)!=7:
            cols.append(i)
        else:
            # display(ot[cols].head())
            new_header = indirect[cols].iloc[0] #grab the first row for the header
            # display(new_header)

            df = indirect[cols][2:] #take the data less the header row
            df.columns = new_header #set the header row as the df header
            # display(df.head())

            # only process if normal hours clocked in that month
            if 'Normal time (Non Mgt)CATS' in df.columns:
                # Replace NAN with 0
                df.dropna(subset = ['Normal time (Non Mgt)CATS'], inplace=True) 

                df['Percentage Overtime'] = df.apply(lambda row: percentage(row), axis=1)
                df.sort_values(by=['Percentage Overtime'], ascending = False, inplace=True)
                df = df.rename(columns={np.nan: 'Craft'})
                # Save in dict
                dict[i] = df.head()
            else:
                # If no normal hours clocked, put an empty array in the dict as value
                dict[i] = []

            # Contains columns for each month
            cols = []
            cols.append('Unnamed: 1')
            cols.append(i)

# Store data (serialize)
with open('craftwise_overtime_indirect.pickle', 'wb') as handle:
    pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

dict = {}


cols = []
start = 1
for i in direct.iloc[:, 3:].columns:
    if start:
        cols.append('Unnamed: 1')
        cols.append(i)
        start = 0
    else:
        if len(i)!=7:
            cols.append(i)
        else:
            # display(ot[cols].head())
            new_header = direct[cols].iloc[0] #grab the first row for the header
            # display(new_header)

            df = direct[cols][2:] #take the data less the header row
            df.columns = new_header #set the header row as the df header
            # display(df.head())

            # only process if normal hours clocked in that month
            if 'Normal time (Non Mgt)CATS' in df.columns:
                # Replace NAN with 0
                df.dropna(subset = ['Normal time (Non Mgt)CATS'], inplace=True) 

                df['Percentage Overtime'] = df.apply(lambda row: percentage(row), axis=1)
                df.sort_values(by=['Percentage Overtime'], ascending = False, inplace=True)
                df = df.rename(columns={np.nan: 'Craft'})

                # Save in dict
                dict[i] = df.head()
            else:
                # If no normal hours clocked, put an empty array in the dict as value
                dict[i] = []

            # Contains columns for each month
            cols = []
            cols.append('Unnamed: 1')
            cols.append(i)

# Store data (serialize)
with open('craftwise_overtime_direct.pickle', 'wb') as handle:
    pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# ## The program makes a dictionary with months as keys, and the values are top 5 crafts clocking in the most hours as overtime hours
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import networkx as nx
# import plotly.graph_objs as go
# from IPython.display import display
# import numpy as np
# import matplotlib.pyplot as plt
# import collections
# import pandas as pd
# from colour import Color
# from datetime import datetime
# from textwrap import dedent as d
# import json
# import re
# import pickle

# def percentage(row):
#     ## Place 0's where Nan so that we can add the values
#     row = row.fillna(0)   
#     ## Rounding the results to 2 decimal places
#     return round((sum(row[2:])/sum(row[1:])*100),1)

# # Read the data file
# ot = pd.read_excel("./Craftwise_Overtime_Direct.xlsx")

# dict = {}


# cols = []
# start = 1
# for i in ot.iloc[:, 2:].columns:
#     if start:
#         cols.append('Calendar Year/Month')
#         cols.append(i)
#         start = 0
#     else:
#         if len(i)!=7:
#             cols.append(i)
#         else:
#             # display(ot[cols].head())
#             new_header = ot[cols].iloc[0] #grab the first row for the header
#             df = ot[cols][2:] #take the data less the header row
#             df.columns = new_header #set the header row as the df header
#             # display(df.head())

#             # only process if normal hours clocked in that month
#             if 'Normal time (Non Mgt)CATS' in df.columns:
#                 # Replace NAN with 0
#                 df.dropna(subset = ['Normal time (Non Mgt)CATS'], inplace=True) 

#                 df['Percentage Overtime'] = df.apply(lambda row: percentage(row), axis=1)
#                 df.sort_values(by=['Percentage Overtime'], ascending = False, inplace=True)

#                 # Save in dict
#                 dict[i] = df.head()
#             else:
#                 # If no normal hours clocked, put an empty array in the dict as value
#                 dict[i] = []

#             # Contains columns for each month
#             cols = []
#             cols.append('Calendar Year/Month')
#             cols.append(i)

# # Store data (serialize)
# with open('craftwise_overtime_direct.pickle', 'wb') as handle:
#     pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# ot = pd.read_excel("./Craftwise_Overtime_Indirect.xlsx")

# dict = {}


# cols = []
# start = 1
# for i in ot.iloc[:, 2:].columns:
#     if start:
#         cols.append('Calendar Year/Month')
#         cols.append(i)
#         start = 0
#     else:
#         if len(i)!=7:
#             cols.append(i)
#         else:
#             # display(ot[cols].head())
#             new_header = ot[cols].iloc[0] #grab the first row for the header
#             df = ot[cols][2:] #take the data less the header row
#             df.columns = new_header #set the header row as the df header
#             # display(df.head())

#             # only process if normal hours clocked in that month
#             if 'Normal time (Non Mgt)CATS' in df.columns:
#                 # Replace NAN with 0
#                 df.dropna(subset = ['Normal time (Non Mgt)CATS'], inplace=True) 

#                 df['Percentage Overtime'] = df.apply(lambda row: percentage(row), axis=1)
#                 df.sort_values(by=['Percentage Overtime'], ascending = False, inplace=True)

#                 # Save in dict
#                 dict[i] = df.head()
#                 display(i, df.head())
#             else:
#                 # If no normal hours clocked, put an empty array in the dict as value
#                 dict[i] = []

#             # Contains columns for each month
#             cols = []
#             cols.append('Calendar Year/Month')
#             cols.append(i)

# # Store data (serialize)
# with open('craftwise_overtime_indirect.pickle', 'wb') as handle:
#     pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


