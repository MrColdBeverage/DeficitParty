# Import packages
from bokeh.core.property.numeric import Interval
from bokeh.io.output import reset_output
from bokeh.models.annotations import Label, LabelSet
from bokeh.models.glyphs import VArea
from bokeh.models.layouts import Panel
from bokeh.models.tickers import SingleIntervalTicker
import numpy as np
import pandas as pd
import datetime as dt
import os
from bokeh.io import output_file, save
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, CDSView, GroupFilter, Title,
                          Legend, HoverTool, NumeralTickFormatter,Span, Tabs, Panel)

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(cur_path, 'data')
party_data_path = os.path.join(data_dir, 'deficit_party_data.csv')
images_dir = os.path.join(cur_path, 'images')
deficit_plots_dir = os.path.join(images_dir, 'deficit_plots')

#Reading data from CVS (deficit_party_data.csv)
source=[]
cds_list=[]
for i in range(6):
    source.append(pd.read_csv(party_data_path,
                         dtype={'Year': np.int64,
                                'deficit_gdp': np.float64,
                                'receipts_gdp': np.float64,
                                'spend_int_gdp': np.float64,
                                'spend_nonint_gdp': np.float64,
                                'spend_tot_gdp': np.float64,
                                'president': 'str',
                                'president_party': 'str',
                                'congress_num': np.int64,
                                'congress_sess': np.int64,
                                'dem_whitehouse': np.int64,
                                'dem_senateseats': np.int64,
                                'rep_senateseats': np.int64,
                                'oth_senateseats': np.int64,
                                'tot_senateseats': np.int64,
                                'dem_houseseats': np.int64,
                                'rep_houseseats': np.int64,
                                'oth_houseseats': np.int64,
                                'tot_houseseats': np.int64},
                         skiprows=3))
    cds_list.append(ColumnDataSource(source[i]))

def output(title, file_name):
    fig_path = os.path.join(deficit_plots_dir, file_name)
    output_file(fig_path, title=title)

# Returns a list of 3 figures with the given title
def generateFigures(title, x_label, y_label, min_seats, max_seats, min_y, max_y):
    fig_list=[]
    for i in range(3):
        fig = figure(title=title,
             plot_height=600,
             plot_width=1200,
             x_axis_label=x_label,
             x_range=(min_seats-3, max_seats+3),
             y_axis_label=y_label,
             y_range=(min_y-4, max_y+4),
             tools=['zoom_in', 'zoom_out', 'box_zoom',
                    'pan', 'undo', 'redo', 'reset'],
             toolbar_location='right')
        
        # Set title font size and axes font sizes
        fig.title.text_font_size = '18pt'
        fig.xaxis.axis_label_text_font_size = '12pt'
        fig.xaxis.major_label_text_font_size = '12pt'
        fig.yaxis.axis_label_text_font_size = '12pt'
        fig.yaxis.major_label_text_font_size = '12pt'
        # Modify tick intervals for X-axis and Y-axis
        fig.xaxis.ticker=SingleIntervalTicker(interval=10, num_minor_ticks=0)
        fig.xgrid.ticker=SingleIntervalTicker(interval=10)
        fig.yaxis.ticker=SingleIntervalTicker(interval=5, num_minor_ticks=0)
        fig.ygrid.ticker=SingleIntervalTicker(interval=10)
        # Disable Scrolling
        fig.toolbar.active_drag = None
        # Remove Logo from toolbar
        fig.toolbar.logo = None

        fig_list.append(fig)
    return fig_list

def plotCircle(i, x_value, y_value, fig, color,src):
    if(color == 'red'):
        LEGEND_LABEL = 'Republican Control'
    elif(color == 'blue'):
        LEGEND_LABEL = 'Democrat Control'
    else:
        LEGEND_LABEL = 'Split Control'

    fig.circle( x=source[src][x_value][i],
                y=source[src][y_value][i],
                size=10,
                line_width=1,
                line_color='black',
                fill_color=color,
                alpha=0.7,
                muted_alpha=0.1,
                legend_label = LEGEND_LABEL)

def deficitPlots(deficit_component, seat_type, src):
    # Check input
    if(not(deficit_component == 'deficit' or deficit_component == 'spending' or deficit_component == 'revenues')
        or not(seat_type == 'house' or seat_type == 'senate')):
        print('invalid input')
        return

    # Define variables for plot
    data_length = len(source[src]['Year'])
    starting_index=0
    if(seat_type=='house'):
        half_line = 217
        x_label='Number of Democratic House Seats (out of 435)'
        x_value = 'DemHouseSeats'
        min_seats = source[src][x_value].min()
        max_seats = source[src][x_value].max()
        if(deficit_component=='deficit'):
            fig_title='U.S. Federal Deficits as Percent of Gross Domestic Product by Democrat House Seats: 1929-2020'
            file_name="house_deficit_plot.html"
            y_label='Deficit / GDP'
            y_value = 'deficit_gdp'
            min_y = source[src][y_value].min()
            max_y = source[src][y_value].max()
        elif(deficit_component=='spending'):
            fig_title='U.S. Federal Noninterest Spending as Percent of Gross Domestic Product by Democrat House Seats: 1929-2020'
            file_name="house_noninterest-spending_plot.html"
            y_label='Noninterest Spending / GDP'
            y_value = 'spend_nonint_gdp'
            min_y = source[src][y_value].min()
            max_y = source[src][y_value].max()
            starting_index=11
        elif(deficit_component=='revenues'):
            fig_title='U.S. Federal Receipts as Percent of Gross Domestic Product by Democrat House Seats: 1929-2020'
            file_name="house_revenues_plot.html"
            y_label='Receipts / GDP'
            y_value = 'receipts_gdp'
            min_y = source[src][y_value].min()
            max_y = source[src][y_value].max()
    else:
        half_line=50
        x_label='Number of Democratic Senate Seats (out of 100)'
        x_value = 'DemSenateSeats'
        min_seats = source[src][x_value].min()
        max_seats = source[src][x_value].max()
        if(deficit_component=='deficit'):
            fig_title='U.S. Federal Deficits as Percent of Gross Domestic Product by Democrat Senate Seats: 1929-2020'
            file_name="senate_deficit_plot.html"
            y_label='Deficit / GDP'
            y_value = 'deficit_gdp'
            min_y = source[src][y_value].min()
            max_y = source[src][y_value].max()
        elif(deficit_component=='spending'):
            fig_title='U.S. Federal Noninterest Spending as Percent of Gross Domestic Product by Democrat Senate Seats: 1929-2020'
            file_name="senate_noninterest-spending_plot.html"
            y_label='Noninterest Spending / GDP'
            y_value = 'spend_nonint_gdp'
            min_y = source[src][y_value].min()
            max_y = source[src][y_value].max()
            starting_index=11
        elif(deficit_component=='revenues'):
            fig_title='U.S. Federal Receipts as Percent of Gross Domestic Product by Democrat Senate Seats: 1929-2020'
            file_name="senate_revenues_plot.html"
            y_label='Receipts / GDP'  
            y_value = 'receipts_gdp' 
            min_y = source[src][y_value].min()
            max_y = source[src][y_value].max()   

    # Generate Figures
    fig_list=[]
    fig_list = generateFigures(fig_title, x_label, y_label, min_seats, max_seats, min_y, max_y)

    # Vertical black line noting half of senate seats
    halfLine = Span(location=half_line,dimension='height',line_color='black',line_width=2)
    for i in range(3):
        fig_list[i].add_layout(halfLine)
    
    # Plot data points
    for n in range(3):
        for i in range(starting_index, data_length):
            if(n==0):
                if(source[src]["DemHouseSeats"][i] < 217 and source[src]["DemSenateSeats"][i] < 50 and source[src]["DemWhitehouse"][i] == 0):
                    plotCircle(i,x_value, y_value, fig_list[n], 'red',src)
                elif (source[src]["DemHouseSeats"][i] > 217 and source[src]["DemSenateSeats"][i] > 50 and source[src]["DemWhitehouse"][i] == 1):
                    plotCircle(i,x_value, y_value, fig_list[n], 'blue',src)
                else:
                    plotCircle(i,x_value, y_value, fig_list[n], 'green',src)
            elif(n==1):
                if(source[src]["DemSenateSeats"][i] < 50 and source[src]["DemWhitehouse"][i] == 0):
                    plotCircle(i,x_value, y_value, fig_list[n], 'red',src)
                elif (source[src]["DemSenateSeats"][i] > 50 and source[src]["DemWhitehouse"][i] == 1):
                    plotCircle(i,x_value, y_value, fig_list[n], 'blue',src)
                else:
                    plotCircle(i,x_value, y_value, fig_list[n], 'green',src)
            elif(n==2):
                if(source[src]["DemHouseSeats"][i] < 217 and source[src]["DemWhitehouse"][i] == 0):
                    plotCircle(i,x_value, y_value, fig_list[n], 'red',src)
                elif (source[src]["DemHouseSeats"][i] > 217 and source[src]["DemWhitehouse"][i] == 1):
                    plotCircle(i,x_value, y_value, fig_list[n], 'blue',src)
                else:
                    plotCircle(i,x_value, y_value, fig_list[n], 'green',src)
                    
    # Set up hover tool for each figure
    TOOLTIPS = [('Year', '@Year'),
                ('Deficit over GDP', '@deficit_gdp{0.0}'+'%'),
                ('President','@President'),
                ('White House', '@PresidentParty'),
                ('Rep. House Seats', '@RepHouseSeats'),
                ('Dem. House Seats', '@DemHouseSeats'),
                ('Rep. Senate Seats', '@RepSenateSeats'),
                ('Dem. Senate Seats', '@DemSenateSeats')]
    for i in range(3):
        fig_list[i].scatter(x=x_value, y=y_value, source=cds_list[src], 
                size=20, alpha=0, name='hover_trigger')
        fig_list[i].add_tools(HoverTool(tooltips=TOOLTIPS, names=['hover_trigger']))
    
   # Set up legend for each figure
    for i in range(3):
        fig_list[i].legend.location = 'bottom_right'
        fig_list[i].legend.border_line_width = 2
        fig_list[i].legend.border_line_color = 'black'
        fig_list[i].legend.border_line_alpha = 1
        fig_list[i].legend.label_text_font_size = '4mm'
        # Set legend muting click policy
        fig_list[i].legend.click_policy = 'mute'

    # Add notes below plot
    for i in range(3):
        #Add notes below image
        note_text_1 = ('Note: Republican control in a given year is defined as the ' +
                    'President being Republican and Republicans holding more ' +
                    'than 217 House seats for the majority of that year.')
        caption1 = Title(text=note_text_1, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption1, 'below')
        note_text_2 = ('   Democrat control is defined as the President being ' +
                    'Democrat and Democrats holding more than 217 House seats ' +
                    'for the majority of that year. Split government is')
        caption2 = Title(text=note_text_2, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption2, 'below')
        note_text_3 = ('   defined as one party holding the White ' +
                    'House while the other party holds a majority of House seats.')
        caption3 = Title(text=note_text_3, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption3, 'below')
        note_text_4 = ('Source: Federal Reserve Economic Data (FRED, FYFRGDA188S), ' +
                    'United States House of Representatives History, Art, & ' +
                    'Archives, "Party Divisions of the House of')
        caption4 = Title(text=note_text_4, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption4, 'below')
        note_text_5 = ('   Representatives, 1789 to present", '+ 
                    'https://history.house.gov/Institution/Party-Divisions/Party-Divisions/, '+
                    'Richard W. Evans (@rickecon).')
        caption5 = Title(text=note_text_5, align='left', text_font_size='4mm',
                        text_font_style='italic')
        fig_list[i].add_layout(caption5, 'below')
    
    # Output figures to an HTML file
    output(fig_title, file_name)

    panel_list=[]
    panel_list.append(Panel(child=fig_list[0], title='Full Control'))
    panel_list.append(Panel(child=fig_list[1], title='Senate Control'))
    panel_list.append(Panel(child=fig_list[2], title='House Control'))

    save(Tabs(tabs=panel_list))


#________________________________________
#Function Calls
#________________________________________
deficitPlots('deficit','senate',0)
deficitPlots('revenues','senate',1)
deficitPlots('spending','senate',2)
deficitPlots('deficit','house',3)
deficitPlots('revenues','house',4)
deficitPlots('spending','house',5)
