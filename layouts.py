import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_table
from dash_table.Format import Format, Group
import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from app import app
from callbacks import s_graph, cats_graph, crafts_direct_table_data, crafts_indirect_table_data, time_division_graph, total_time_graph, network_graph, graph_degree, total_salary_graph, salary_s_graph,employee_count_graph, table_style,table_data, table_columns



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
    'margin-left' : '15px',
    'margin-right' : '15px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['dark-blue'],
    'background-color' : corporate_colors['blue'],
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
    'text-decoration-color' : corporate_colors['blue'],
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
    'background-color' : 'rgb(251, 251, 252, 0.1)'
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
# 000 - IMPORT DATA
####################################################################################################

####################################################################################################
# 000 - DEFINE REUSABLE COMPONENTS AS FUNCTIONS
####################################################################################################

#####################
# Header with logo
def get_header():

    header = html.Div([

        html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H1(children='Piperack 1555 Dashboard',
                    style = {'textAlign' : 'center',
                            'color':'black'}
            )],
            className='col-8',
            style = {'padding-top' : '1%'}
        ),

        html.Div([
            html.Img(
                    src = app.get_asset_url('Descon_logo.png'),
                    height = '43 px',
                    width = 'auto')
            ],
            className = 'col-2',
            style = {
                    'align-items': 'center',
                    'padding-top' : '1%',
                    'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%',
                'background-color' : corporate_colors['white']}
        )

    return header

#####################
# Nav bar
def get_navbar(p = 'sales'):

    navbar_sales = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Home',
                        style = navbarcurrentpage),
                href='/apps/sales-overview'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Heirarchy Chart'),
                href='/apps/hchart'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Time sheet'),
                href='/apps/tsheet'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : corporate_colors['red'],
            'box-shadow': '2px 5px 5px 1px rgba(100, 101, 131, .5)'}
    )

    navbar_page2 = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Home'),
                href='/apps/sales-overview'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Heirarchy Chart'),
                href='/apps/hchart'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Time sheet'),
                href='/apps/tsheet'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : corporate_colors['red'],
            'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    navbar_page3 = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Home'),
                href='/apps/sales-overview'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Heirarchy Chart'),
                href='/apps/hchart'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Time sheet'),
                href='/apps/tsheet'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : corporate_colors['red'],
            'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    if p == 'sales':
        return navbar_sales
    elif p == 'page2':
        return navbar_page2
    else:
        return navbar_page3

#####################
# Empty row

def get_emptyrow(h='45px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow

####################################################################################################
# 001 - SALES
####################################################################################################

sales = html.Div([

    #####################
    #Row 1 : Header
    get_header(),

    #####################
    #Row 2 : Nav bar
    get_navbar('sales'),

    #####################
    #Row 3 : Filters
    html.Div([ # External row

        html.Div([ # External 12-column

            html.Div([ # Internal row

                #Internal columns
                html.Div([
                ],
                className = 'col-2'), # Blank 2 columns

            ],
            className = 'row') # Internal row

        ],
        className = 'col-12',
        style = filterdiv_borderstyling) # External 12-column

    ],
    className = 'row sticky-top'), # External row

    #####################
    #Row 4
    get_emptyrow(),

    #####################
    #Row 5 : Charts
    html.Div([ # External row

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

        html.Div([ # External 10-column

            html.H2(children = " Project Overview",
                    style = {'color' : corporate_colors['white']}),

            html.Div([ # Internal row - RECAPS

                html.Div([],className = 'col-4'), # Empty column

                html.Div([
                    dash_table.DataTable(
                        id='recap-table',
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
                        data = table_data(),
                        columns = table_columns(),
                        style_data_conditional = table_style()
                    )
                ],
                className = 'col-4'),

                html.Div([],className = 'col-4') # Empty column

            ],
            className = 'row',
            style = recapdiv
            ), # Internal row - RECAPS

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(id="s-graph",
                            figure=s_graph())
                ],
                className = 'col-6'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='time-graph',
                            figure=total_time_graph())
                ],
                className = 'col-6'),

            ],
            className = 'row'), # Internal row

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='salary-s-graph',
                        figure=salary_s_graph())
                ],
                className = 'col-6'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='monthly-salary-graph',
                            figure=total_salary_graph())
                ],
                className = 'col-6'),

            ],
            className = 'row'), # Internal row

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='employee-count',
                        figure=employee_count_graph())
                ],
                className = 'col-6'),

            ],
            className = 'row') # Internal row

        ],
        className = 'col-10',
        style = externalgraph_colstyling), # External 10-column

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

    ],
    className = 'row',
    style = externalgraph_rowstyling
    ), # External row

])

####################################################################################################
# 002 - Page 2
####################################################################################################

page2 = html.Div([

    #####################
    #Row 1 : Header
    get_header(),

    #####################
    #Row 2 : Nav bar
    get_navbar('page2'),

    #####################
    #Row 3 : Filters
    html.Div([ # External row

        html.Div([ # External 12-column

            html.Div([ # Internal row

                #Internal columns
                html.Div([
                ],
                className = 'col-2'), # Blank 2 columns

                html.Div([
                ],
                className = 'col-2') # Blank 2 columns


            ],
            className = 'row') # Internal row

        ],
        className = 'col-12',
        style = filterdiv_borderstyling) # External 12-column

    ],
    className = 'row sticky-top'), # External row

    #####################
    #Row 4
    get_emptyrow(),

    #####################
    #Row 5 : Charts
    html.Div([ # External row

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

        html.Div([ # External 10-column

            html.H2(children = "Heirachy Chart",
                    style = {'color' : corporate_colors['white']}),

            html.Div([ # Internal row - RECAPS

                html.Div([],className = 'col-4'), # Empty column
                html.Div([
                    dcc.Checklist(
                        id = "data-type",
                        options=[
                            {'label': 'Include Non Management', 'value': 'NM'},
                        ],
                        value=['NM']
                    )  
                ],className = 'col-4')
                

            ],
            className = 'row',
            style = recapdiv
            ), # Internal row - RECAPS

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(id="my-graph",
                            figure=network_graph())
                ],
                className = 'col-12'),
            ],
            className = 'row'), # Internal row

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(id="my-graph2",
                        figure=graph_degree())
                ],
                className = 'col-7'),

               
            ],
            className = 'row') # Internal row


        ],
        className = 'col-10',
        style = externalgraph_colstyling), # External 10-column

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

    ],
    className = 'row',
    style = externalgraph_rowstyling
    ), # External row

])

####################################################################################################
# 003 - Page 3
####################################################################################################

page3 = html.Div([

    #####################
    #Row 1 : Header
    get_header(),

    #####################
    #Row 2 : Nav bar
    get_navbar('page3'),

    #####################
    #Row 3 : Filters
    html.Div([ # External row

        html.Div([ # External 12-column

            html.Div([ # Internal row

                #Internal columns
                html.Div([
                ],
                className = 'col-2'), # Blank 2 columns

                html.Div([
                ],
                className = 'col-2') # Blank 2 columns


            ],
            className = 'row') # Internal row

        ],
        className = 'col-12',
        style = filterdiv_borderstyling) # External 12-column

    ],
    className = 'row sticky-top'), # External row

    #####################
    #Row 4
    get_emptyrow(),

    #####################
    #Row 5 : Charts
    html.Div([ # External row

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

        html.Div([ # External 10-column

            html.H2(children = "Project Timesheet and crafts",
                    style = {'color' : corporate_colors['white']}),

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(id="cats-graph",
                        figure=cats_graph())
                ],
                className = 'col-9'),

                # Chart Column
                html.Div([
                    dcc.Graph(id="time-division-graph",
                            figure=time_division_graph(""))
                ],
                className = 'col-3'),

            ],
            className = 'row'), # Internal row

            html.Div([ # Internal row - RECAPS

                html.Div([],className = 'col-4'), # Empty column
                html.H4(children = "Direct Employees",
                    style = {'color' : corporate_colors['white']}),
                html.Div(id="direct-employees-table"),
                html.Div([],className = 'col-4') # Empty column

            ],
            className = 'row',
            style = recapdiv
            ), # Internal row - RECAPS

            html.Div([ # Internal row - RECAPS

                html.Div([],className = 'col-4'), # Empty column
                html.H4(children = "Indirect Employees",
                    style = {'color' : corporate_colors['white']}),
                html.Div(id="indirect-employees-table"),
                html.Div([],className = 'col-4') # Empty column

            ],
            className = 'row',
            style = recapdiv
            ), # Internal row - RECAPS
        ],
        className = 'col-10',
        style = externalgraph_colstyling), # External 10-column

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

    ],
    className = 'row',
    style = externalgraph_rowstyling
    ), # External row

])