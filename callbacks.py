import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_table
from dash_table.Format import Format, Group, Scheme
import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from app import app
from datetime import datetime
import plotly.graph_objects as px
import pickle
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from colour import Color
from datetime import datetime
import textwrap
import json
import re
import collections
from IPython.display import display

####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

####################### Corporate css formatting
corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'blue' : 'rgb(34, 90, 163)',
    'red' : 'rgb(232, 79, 79)',
    'dark-blue' : 'rgb(23, 140, 156)',
    'medium-blue-grey' : 'rgb(79, 138, 232)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}

externalgraph_rowstyling = {
    'margin-left' : '12px',
    'margin-right' : '12px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['white'],
    'background-color' : corporate_colors['white'],
    'box-shadow' : '0px 0px 17px 0px rgba(186, 218, 212, .5)',
    'padding-top' : '10px'
}

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['light-green'],
    'background-color' : corporate_colors['light-green'],
    'box-shadow' : '2px 5px 5px 1px rgba(255, 101, 131, .5)'
    }

navbarcurrentpage = {
    'text-decoration' : 'underline',
    'text-decoration-color' : corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
    }

recapdiv = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'rgb(251, 251, 252, 0.1)',
    'margin-left' : '15px',
    'margin-right' : '15px',
    'margin-top' : '15px',
    'margin-bottom' : '15px',
    'padding-top' : '5px',
    'padding-bottom' : '5px',
    'background-color' : 'rgb(51, 251, 252, 0.1)'
    }

recapdiv_text = {
    'text-align' : 'left',
    'font-weight' : '350',
    'color' : corporate_colors['white'],
    'font-size' : '1.5rem',
    'letter-spacing' : '0.04em'
    }

####################### Corporate chart formatting

corporate_title = {
    'font' : {
        'size' : 16,
        'color' : corporate_colors['white']}
}

corporate_xaxis = {
    'showgrid' : False,
    'linecolor' : corporate_colors['light-grey'],
    'color' : corporate_colors['light-grey'],
    'tickangle' : 315,
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_yaxis = {
    'showgrid' : True,
    'color' : corporate_colors['light-grey'],
    'gridwidth' : 0.5,
    'gridcolor' : corporate_colors['dark-green'],
    'linecolor' : corporate_colors['light-grey'],
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_font_family = 'Dosis'

corporate_legend = {
    'orientation' : 'h',
    'yanchor' : 'bottom',
    'y' : 1.01,
    'xanchor' : 'right',
    'x' : 1.05,
	'font' : {'size' : 9, 'color' : corporate_colors['light-grey']}
} # Legend will be on the top right, above the graph, horizontally

corporate_margins = {'l' : 5, 'r' : 5, 't' : 45, 'b' : 15}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    font = {'family' : corporate_font_family},
    title = corporate_title,
    title_x = 0.5, # Align chart title to center
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis = corporate_xaxis,
    yaxis = corporate_yaxis,
    height = 270,
    legend = corporate_legend,
    margin = corporate_margins
    )

####################################################################################################
# 000 - DATA MAPPING
####################################################################################################

#Sales mapping
sales_filepath = 'data/datasource.xlsx'

sales_fields = {
    'date' : 'Date',
    'reporting_group_l1' : 'Country',
    'reporting_group_l2' : 'City',
    'sales' : 'Sales Units',
    'revenues' : 'Revenues',
    'sales target' : 'Sales Targets',
    'rev target' : 'Rev Targets',
    'num clients' : 'nClients'
    }
sales_formats = {
    sales_fields['date'] : '%d/%m/%Y'
}
####################################################################################################
# 000 - IMPORT DATA
####################################################################################################

data = pd.read_excel("./data/final_data.xlsx")

# Used for Hours data, Salary Data, Employee COunt data
ot = pd.read_excel("./data/salary_time_count.xlsx", dtype={'Calendar Year/Month': str,})

ot = ot.fillna(0)
d1 = str(ot.iloc[0,0])
d1 = datetime.strptime(d1, '%m.%Y')
d2 = str(ot.iloc[-1,0])
d2 = datetime.strptime(d2, '%m.%Y')
ot['time_sum']=  ot['Payroll Hrs'].cumsum()
ot['salary_sum']=  ot['Amount'].cumsum()
ot = ot.set_index('Calendar Year/Month')

time_division = pd.read_excel("./data/Cats.xlsx")
time_division = time_division.iloc[:, :-1].fillna(0).drop([0])

def lookup_name(given):
    value = data2[(data2['Employee']==given)]
    if len(value)>0:
        return value.iloc[0,1]
    else:
        return "NA"

def lookup_position(given):
    value = data2[(data2['Employee']==given)]
    # if (given == '106832'):
    #     display(value)
    if len(value)>0:
        return value.iloc[0,4]
    else:
        return "NA"

# Used for Displaying Overtime crafts in each month
with open('./data/craftwise_overtime_indirect.pickle', 'rb') as handle:
    craftwise_overtime_indirect = pickle.load(handle)

# Used for Displaying Overtime crafts in each month
with open('./data/craftwise_overtime_direct.pickle', 'rb') as handle:
    craftwise_overtime_direct = pickle.load(handle)

## Data2 is there to lookup the positions and employee names
data2 = data
data2['Employee'] = data2['Employee'].astype(str)

## Remove employees reporting to themselves
data['Employee'] = data['Employee'].astype(str)
data = data[data['Employee'] != data['Supervisor ID']]

## Global variable storing whether to display NM or M employees
EMPLOY = ['M', 'NM']

e = pd.DataFrame()
e['Source'] = data['Employee']
e['Target'] = data['Supervisor ID']
e['TransactionAmt'] = 100

n = pd.DataFrame()
n['Account'] = pd.concat([data['Employee'], data['Supervisor ID']]).unique()
n['EmployeeName'] = n.apply (lambda row: lookup_name(row['Account']), axis=1)
n['Type'] = n.apply (lambda row: lookup_position(row['Account']), axis=1)

################################################################################################################################################## SET UP END

####################################################################################################
# 000 - DEFINE ADDITIONAL FUNCTIONS
####################################################################################################
def colorscale_generator(n, starting_col = {'r' : 186, 'g' : 218, 'b' : 212}, finish_col = {'r' : 57, 'g' : 81, 'b' : 85}):
    """This function generate a colorscale between two given rgb extremes, for an amount of data points
    The rgb should be specified as dictionaries"""
    r = starting_col['r']
    g = starting_col['g']
    b = starting_col['b']
    rf = finish_col['r']
    gf = finish_col['g']
    bf = finish_col['b']
    ri = (rf - r) / n
    gi = (gf - g) / n
    bi = (bf - b) / n
    color_i = 'rgb(' + str(r) +','+ str(g) +',' + str(b) + ')'
    my_colorscale = []
    my_colorscale.append(color_i)
    for i in range(n):
        r = r + ri
        g = g + gi
        b = b + bi
        color = 'rgb(' + str(round(r)) +','+ str(round(g)) +',' + str(round(b)) + ')'
        my_colorscale.append(color)

    return my_colorscale

# Create a corporate colorcale
colors = colorscale_generator(n=11)

corporate_colorscale = [
    [0.0, colors[0]],
    [0.1, colors[1]],
    [0.2, colors[2]],
    [0.3, colors[3]],
    [0.4, colors[4]],
    [0.5, colors[5]],
    [0.6, colors[6]],
    [0.7, colors[7]],
    [0.8, colors[8]],
    [0.9, colors[9]],
    [1.0, colors[10]]]


def graph_degree():
# """This function produces a graph showing the degree of the heirarichal chart graph"""
    node1 = n
    edge1 = e

    # Filter only management employees
    if len(EMPLOY)==0:
        edge1 = edge1[edge1['Source'].str.startswith('1')]

    G = nx.from_pandas_edgelist(edge1, 'Source', 'Target', ['Source', 'Target', 'TransactionAmt',], create_using=nx.MultiDiGraph())
    nx.set_node_attributes(G, node1.set_index('Account')['EmployeeName'].to_dict(), 'EmployeeName')
    nx.set_node_attributes(G, node1.set_index('Account')['Type'].to_dict(), 'Type')

    pos = graphviz_layout(G, prog="dot")

    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])
    
    # display(G.in_degree())
    degree_sequence = sorted([d for n, d in G.in_degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    cnt, deg = zip(*degreeCount.items())
    
    deg = [str(x) for x in deg]
    i = 0
    while i < len(deg):
        deg[i] = str(deg[i])
        deg[i] += "`"*i
        i+=1
    f = deg

    fig = go.Figure(go.Bar(
        x = f,
        y = cnt,
        hovertemplate="%{x} is/are supervising %{y} employees<extra></extra>",
        marker = {'color' : corporate_colors['pink-red'], 'opacity' : 0.75},
        ),
        layout=corporate_layout,
    )
    fig.update_xaxes(title_text="Number of people Supervising")
    fig.update_yaxes(title_text="Count")
    fig.update_layout(barmode='group')
    fig.update_layout(
        title={'text' : "Supervisor Employee count chart"},
        showlegend = False)
    return fig

####################################################################################################
# 001 - Used in Timesheet to display bar chart containg NT OT and SOT for each month
####################################################################################################
def cats_graph():  
    fig = px.Figure(layout=corporate_layout)
    x = []
    nt = []
    ot = []
    sot = []
    for beg in pd.date_range(d1, d2, freq='MS'):
            beg = beg.to_pydatetime()
            month = beg.strftime("%m.%Y")
            x.append(beg)
            nt.append(time_division[month].iloc[0])
            ot.append(time_division[month].iloc[2])
            sot.append(time_division[month].iloc[3])

    fig = fig.add_trace(px.Bar(x=x, y=nt, text = nt, 
                            textposition = 'inside', name = "Normal Time"
                            ))
    fig = fig.add_trace(px.Bar(x=x, y=ot, text = ot, 
                                textposition = 'inside', name = "Over Time"))
    fig = fig.add_trace(px.Bar(x=x, y=sot, text = sot, 
                                textposition = 'inside', name = "Special Over Time"))
    fig.update_layout(hovermode='x')    
    return fig

####################################################################################################
# 001 - Used on homepage. S-curve for total hours put in the project
####################################################################################################
def s_graph():  
    fig = px.Figure(layout=corporate_layout)
    x=[]
    y=[]

    for beg in pd.date_range(d1, d2, freq='MS'):
            beg = beg.to_pydatetime()
            month = beg.strftime("%m.%Y")
            x.append(beg)
            y.append(ot.loc[month]['time_sum'])


    fig = fig.add_trace(px.Scatter(x=x, y=y, text = 'Total hours', 
                            name = "Cumulative time",
                            line = {'color': corporate_colors['pink-red'], 'width' : 2},
                            ))
    fig.update_layout(
        title={'text' : "Total hours on the project"},
        xaxis = {
            'title' : "Month",
        },
        yaxis = {'title' : "Hours"},
        showlegend = False)
    fig.update_layout(hovermode='x')    
    return fig

####################################################################################################
# 001 - Used on Home page. Month wise division of the total hours put in the project
####################################################################################################
def total_time_graph():  
    fig = px.Figure(layout=corporate_layout)
    x=[]
    y=[]

    for beg in pd.date_range(d1, d2, freq='MS'):
            beg = beg.to_pydatetime()
            month = beg.strftime("%m.%Y")
            x.append(beg)
            y.append(ot.loc[month]['Payroll Hrs'])


    fig = fig.add_trace(px.Bar(x=x, y=y, text = 'Total hours', 
                            name = "Cumulative time",
                            marker = {'color' : corporate_colors['pink-red'], 'opacity' : 0.75},
                            ))

    fig.update_layout(
        title={'text' : "Monthwise distribution of Hours"},
        xaxis = {
            'title' : "Month",
        },
        yaxis = {'title' : "Hours"},
        showlegend = False)
    fig.update_layout(hovermode='x')    
    return fig

####################################################################################################
# 001 - Used on home page to display s-curve of total cumulative amount paid in Perm Sal G/L account
####################################################################################################
def salary_s_graph():  
    fig = px.Figure(layout=corporate_layout)
    x=[]
    y=[]

    for beg in pd.date_range(d1, d2, freq='MS'):
            beg = beg.to_pydatetime()
            month = beg.strftime("%m.%Y")
            x.append(beg)
            y.append(ot.loc[month]['salary_sum'])


    fig = fig.add_trace(px.Scatter(x=x, y=y, text = 'Total Salary Bill', 
                            name = "Cumulative Salary",
                            line = {'color': corporate_colors['pink-red'], 'width' : 2},
                            ))
    fig.update_layout(
        title={'text' : "Total Salary Bill of the project"},
        xaxis = {
            'title' : "Month",
        },
        yaxis = {'title' : "Amount(AED)"},
        showlegend = False)
    fig.update_layout(hovermode='x')    
    return fig

####################################################################################################
# 001 - Used on Home page to show month wise distribution of salary cost as bar chart
####################################################################################################
def total_salary_graph():  
    fig = px.Figure(layout=corporate_layout)
    x=[]
    y=[]

    for beg in pd.date_range(d1, d2, freq='MS'):
            beg = beg.to_pydatetime()
            month = beg.strftime("%m.%Y")
            x.append(beg)
            y.append(ot.loc[month]['Amount'])


    fig = fig.add_trace(px.Bar(x=x, y=y, text = 'Monthly Salary', 
                            marker = {'color' : corporate_colors['pink-red'], 'opacity' : 0.75},
                            ))

    fig.update_layout(
        title={'text' : "Monthwise distribution of Salary"},
        xaxis = {
            'title' : "Month",
        },
        yaxis = {'title' : "Amount(AED)"},
        showlegend = False)
    fig.update_layout(hovermode='x')    
    return fig
####################################################################################################
# 001 -# Shows month wise distribution of employee count as bar chart
####################################################################################################

def employee_count_graph():  
    fig = px.Figure(layout=corporate_layout)
    x=[]
    y=[]

    for beg in pd.date_range(d1, d2, freq='MS'):
            beg = beg.to_pydatetime()
            month = beg.strftime("%m.%Y")
            x.append(beg)
            y.append(ot.loc[month]['No of Employee (Cust'])


    fig = fig.add_trace(px.Bar(x=x, y=y, text = 'Monthly Headcount', 
                            marker = {'color' : corporate_colors['pink-red'], 'opacity' : 0.75},
                            ))

    fig.update_layout(
        title={'text' : "Monthwise distribution of Employee count"},
        xaxis = {
            'title' : "Month",
        },
        yaxis = {'title' : "Count"},
        showlegend = False)
    fig.update_layout(hovermode='x')    
    return fig

####################################################################################################
# 002 -Used on Home page. Forms data for table for KPI measurement 
####################################################################################################
def table_data():
    dat = []
    dict = {}
    dict['KPI'] = 'Manpower'
    dict['Actual'] = str(ot['No of Employee (Cust'].max())
    dict['Planned'] = str(226)
    dat.append(dict)

    dict = {}
    dict['KPI'] = 'Peak Manpower Month'
    dict['Actual'] = str(ot['No of Employee (Cust'].idxmax()) 
    dict['Planned'] = '03.2020'
    dat.append(dict)
    return dat
####################################################################################################
# 003 - Used on Home page. Forms columns for table for KPI measuremen
####################################################################################################
def table_columns():
    columns=[{
            'id': 'KPI',
            'name': 'KPI',
            'type': 'text',
        },{
            'id': 'Actual',
            'name': 'Actual  ',
            'type': 'text'
        }, {
            'id': 'Planned',
            'name': 'Planned',
            'type': 'text',
        },]
    return columns
####################################################################################################
# 004 - Home page. Conditional formatting for KPI table
####################################################################################################
def table_style():
    conditional_style=[
        {'if' : {
            'filter_query' : '{PeakManpower} < {PlannedPeakManpower} && {PlannedPeakManpower} > 0',
            'column_id' : 'PeakManpower'},
        'backgroundColor' : corporate_colors['red'],
        'color' : corporate_colors['red'],
        'fontWeight' : 'bold'
        },
        {'if' : {
            'filter_query' : '{PeakManpower} < {PlannedPeakManpower} && {PlannedPeakManpower} > 0',
            'column_id' : 'PeakManpower'},
        'backgroundColor' : corporate_colors['red'],
        'color' : corporate_colors['pink-red'],
        'fontWeight' : 'bold'
        },
    ]
    return conditional_style

####################################################################################################
# 005 - Time-Sheet. Used on Time sheet page to make the pie shart showing time divsion as percentag
####################################################################################################
def time_division_graph(month): 
    fig = px.Figure(layout=corporate_layout)
    if month!='':
        data = time_division[month]
        labels = ['Normal time','Overtime','Special Overtime']
        values = [data.iloc[0], data.iloc[2], data.iloc[3]]

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)], layout=corporate_layout)
        return fig
   
    return fig

####################################################################################################
# 006 - Time-Sheet. Makes dash datatable for showing direct crafts
####################################################################################################
def crafts_direct_table_data(month):  
    # This function returns a Plotly table that is used to show the top 5 crafts based on the percentage of hours clocked as overtime
    # Month is a string in form "02.2020"
    if month!='':
        if month in craftwise_overtime_direct:
            crafts_data = craftwise_overtime_direct[month]
            if len(crafts_data)==0:
                return []
            else:
                crafts_data = crafts_data.dropna(axis=1,how='all')
                cols = [{"name": i, "id": i,} for i in (crafts_data.columns)]
                
                return [
                    dash_table.DataTable(
                        id='recap-direct',
                        style_table ={
                            'padding-left': '50px',
                        },
                        style_header = {
                            'backgroundColor': 'transparent',
                            'fontFamily' : corporate_font_family,
                            'font-size' : '1rem',
                            'color' : corporate_colors['light-green'],
                            'border': '0px transparent',
                            'textAlign' : 'left',
                            'width' :'auto'
                            },
                        style_cell = {
                            'backgroundColor': 'transparent',
                            'fontFamily' : corporate_font_family,
                            'font-size' : '0.85rem',
                            'color' : corporate_colors['white'],
                            'border': '0px transparent',
                            'height': 'auto',
                            'textAlign' : 'left'},
                        cell_selectable = False,
                        column_selectable = False,
                        data = crafts_data.to_dict('records'),
                        columns = cols,
                    )
                ]
        else:
            return []
    return []

####################################################################################################
# 007 - Time-Sheet Make the dash datatable for displaying the indirect crafts
####################################################################################################
def crafts_indirect_table_data(month):  
    # This function returns a Plotly table that is used to show the top 5 crafts based on the percentage of hours clocked as overtime
    # Month is a string in form "02.2020"
    if month!='':
        if month in craftwise_overtime_indirect:
            crafts_data = craftwise_overtime_indirect[month]
            if len(crafts_data)==0:
                return []
            else:
                crafts_data = crafts_data.dropna(axis=1,how='all')
                cols = [{"name": i, "id": i,} for i in (crafts_data.columns)]

                return [
                    dash_table.DataTable(
                        id='recap-indirect',
                        style_table ={
                            'padding-left': '50px',
                        },
                        style_header = {
                            'backgroundColor': 'transparent',
                            'fontFamily' : corporate_font_family,
                            'font-size' : '1rem',
                            'color' : corporate_colors['light-green'],
                            'border': '0px transparent',
                            'textAlign' : 'left'},
                        style_cell = {
                            'backgroundColor': 'transparent',
                            'fontFamily' : corporate_font_family,
                            'font-size' : '0.85rem',
                            'color' : corporate_colors['white'],
                            'border': '0px transparent',
                            'textAlign' : 'left'},
                        cell_selectable = False,
                        column_selectable = False,
                        data = crafts_data.to_dict('records'),
                        columns = cols,
                    )
                ]
        else:
            return []
    return []

####################################################################################################
# 008 - Heirarchy page. Makes the heirarichal chart
####################################################################################################
def network_graph():  
    node1 = n
    edge1 = e

    # Filter only management employees
    if len(EMPLOY)==0:
        edge1 = edge1[edge1['Source'].str.startswith('1')]


    G = nx.from_pandas_edgelist(edge1, 'Target','Source',  ['Source', 'Target',], create_using=nx.MultiDiGraph())
    nx.set_node_attributes(G, node1.set_index('Account')['EmployeeName'].to_dict(), 'EmployeeName')
    nx.set_node_attributes(G, node1.set_index('Account')['Type'].to_dict(), 'Type')

    pos = graphviz_layout(G, prog="dot",)

    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])


    traceRecode = []  # contains edge_trace, node_trace, middle_node_trace
    colors = list(Color('lightgreen').range_to(Color('lightblue'), len(G.edges())))
    colors = ['rgb' + str(x.rgb) for x in colors]

    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        weight = float(1.8)
        trace = go.Scatter(x=tuple([x1, x0, None]), y=tuple([y1, y0, None]),
                           mode='lines',
                           line={'width': weight,},
                           marker=dict(color=colors[index]),
                           line_shape='spline',
                           opacity=1,)
        traceRecode.append(trace)
        index = index + 1
    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition="bottom center",
                            hoverinfo="text", marker={'size': 30, 'color': 'LightSkyBlue'}, 
                            textfont=dict(family='sans serif',
                                size=10,
                                color='#ffffff',
                                )
                            )

    index = 0

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        hovertext = "E.Name: " + str(node1[node1['Account']==node].iloc[0,1]) + "<br>" + str(node1[node1['Account']==node].iloc[0,0])
        text = str(node1[node1['Account']==node].iloc[0,2])
        _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
        text = _RE_COMBINE_WHITESPACE.sub(" ", text).strip()
        text = "<br>".join(textwrap.wrap(text, width=10))
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])
        index = index + 1

    traceRecode.append(node_trace)

    middle_hover_trace = go.Scatter(x=[], y=[], hovertext=[], mode='markers', hoverinfo="text",
                                    marker={'size': 10, 'color': 'LightSkyBlue'},
                                    opacity=0)

    index = 0
    for edge in G.edges:
        f,t,a = edge
        x0, y0 = G.nodes[edge[1]]['pos']
        x1, y1 = G.nodes[edge[0]]['pos']
        hovertext = "From: " + str(f) + "<br>" + "To: " + str(
            t) 
        middle_hover_trace['x'] += tuple([(x0 + x1) / 2])
        middle_hover_trace['y'] += tuple([(y0 + y1) / 2])
        middle_hover_trace['hovertext'] += tuple([hovertext])
        index = index + 1

    traceRecode.append(middle_hover_trace)
    figure = {
        "data": traceRecode,
        "layout": go.Layout(showlegend=False, hovermode='closest',
                            paper_bgcolor = 'rgba(0,0,0,0)',
                            plot_bgcolor = 'rgba(0,0,0,0)',
                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            clickmode='event+select',
                            annotations=[
                                dict(
                                    ax=(G.nodes[edge[0]]['pos'][0] + G.nodes[edge[1]]['pos'][0]) / 2,
                                    ay=(G.nodes[edge[0]]['pos'][1] + G.nodes[edge[1]]['pos'][1]) / 2, axref='x', ayref='y',
                                    x=(G.nodes[edge[1]]['pos'][0] * 3 + G.nodes[edge[0]]['pos'][0]) / 4,
                                    y=(G.nodes[edge[1]]['pos'][1] * 3 + G.nodes[edge[0]]['pos'][1]) / 4, xref='x', yref='y',
                                    showarrow=True,
                                    arrowhead=2,
                                    arrowsize=3,
                                    arrowwidth=0.5,
                                    opacity=1
                                ) for edge in G.edges]
                            )}
    return figure
####################################################################################################
####################################################################################################
####################################################################################################
# TIMESHEET PAGE
####################################################################################################
####################################################################################################
####################################################################################################
# 001 - Heirarchy page. Toggle management NM staff 
####################################################################################################
@app.callback(
    [dash.dependencies.Output('my-graph', 'figure'),dash.dependencies.Output('my-graph2', 'figure'),],
    [dash.dependencies.Input('data-type', 'value'),])
def update_output(value):
    global EMPLOY
    EMPLOY=value
    return network_graph(), graph_degree()
####################################################################################################
# 001 - Time-Sheet Division into NT OT SOT Percentages pie chart
####################################################################################################
@app.callback(
    dash.dependencies.Output('time-division-graph', 'figure'),
    [dash.dependencies.Input('cats-graph', 'hoverData')])
def display_time_data(hoverData):
    if hoverData is not None:
        month = hoverData['points'][0]['label']
        month = str(datetime.strptime(month, '%Y-%m-%d').strftime("%m.%Y"))
        return time_division_graph(month)
    else:
        return time_division_graph("")

####################################################################################################
# 002 - Time-Sheet Shows direct crafts with most overtime percentage
####################################################################################################
@app.callback(
    dash.dependencies.Output('direct-employees-table', 'children'),
    [dash.dependencies.Input('cats-graph', 'hoverData')])
def display_direct_crafts(hoverData):
    if hoverData is not None:
        month = hoverData['points'][0]['label']
        month = str(datetime.strptime(month, '%Y-%m-%d').strftime("%m.%Y"))
        return crafts_direct_table_data(month)
    else:
        return crafts_direct_table_data("")

####################################################################################################
# 002 - Time-Sheet Shows Indirect crafts with most overtime percentage
####################################################################################################
@app.callback(
    dash.dependencies.Output('indirect-employees-table', 'children'),
    [dash.dependencies.Input('cats-graph', 'hoverData')])
def display_direct_crafts(hoverData):
    if hoverData is not None:
        month = hoverData['points'][0]['label']
        month = str(datetime.strptime(month, '%Y-%m-%d').strftime("%m.%Y"))
        return crafts_indirect_table_data(month)
    else:
        return crafts_indirect_table_data("")



