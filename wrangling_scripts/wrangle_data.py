import plotly.graph_objs as go
from plotly.colors import n_colors
# to handle  data retrieval
import urllib3
from urllib3 import request
# to handle certificate verification
import certifi
# to manage json data
import json
# for pandas dataframes
import pandas as pd

base_url = 'https://www.opendata.nhs.scot/api/3/action/datastore_search_sql?sql='
nbh_id = '8906de12-f413-4b3f-95a0-11ed15e61773'
daily_id = '287fc645-4352-4477-9c8c-55bc054b7e76'
by_hb_id = '427f9a25-db22-4014-a3bc-893b68243055'
hosp_id = '5acbccb1-e9d6-4ab2-a7ac-f3e4d378e7ec'
deaths_id = '733aad2d-5420-4966-bc34-386a3475623f'

def get_api(resource_id, sql_query):
    base_url = 'https://www.opendata.nhs.scot/api/3/action/datastore_search_sql?sql='
    # handle certificate verification and SSL warnings
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    final_url = base_url + sql_query

    r = http.request('GET', final_url)
    # decode json data into a dict object
    data = json.loads(r.data.decode('utf-8'))
    df = pd.json_normalize(data['result']['records'])

    return df

def latest_date(resource_id):
    date_df = get_api(resource_id,
    f'''
    SELECT "Date"
    FROM "{resource_id}"
    ORDER BY "Date" DESC
    LIMIT 1
    ''')
    latest_date = date_df.iloc[0,0]
    return latest_date

def month_before(resource_id,n_days):
    date_df = get_api(resource_id,
    f'''
    SELECT DISTINCT "Date"
    FROM "{resource_id}"
    ORDER BY "Date" DESC
    LIMIT {n_days}
    ''')
    _n_days = date_df.iloc[(n_days-1),0]
    return _n_days

#Daily Cases over time
def daily():
    '''
    returns most recent daily case numbers
    from the Scottish Goverment
    '''
    sql_daily = f'''
    SELECT "Date", "DailyCases"
    FROM "{daily_id}"
    ORDER BY "Date" ASC
    '''
    daily_df = get_api(daily_id, sql_daily)
    daily_df.columns = ['DateStr', 'DailyCases']
    daily_df['Date'] = daily_df['DateStr'].apply(lambda x: pd.to_datetime(str(x),\
        format='%Y%m%d'))
    daily_df = daily_df.drop('DateStr', axis = 1)
    daily_df['AvgCases'] = daily_df['DailyCases'].rolling(14,\
        win_type='triang', min_periods=1).mean()
    return daily_df

#Top Neighbourhoods Daily
def top_nbh_daily():
    '''
    Returns top 50 Neighbourhoods with new cases in Scotland
    according to Scottish Goverment Data
    '''
    day = latest_date(nbh_id)
    sql_nbh = f'''
    SELECT "Date", "IntZoneName", "Positive7Day"
    FROM "{nbh_id}"
    WHERE "Date" = {day}
    '''
    nbh_df = get_api(nbh_id, sql_nbh)
    nbh_df['Positive7Day'] = pd.to_numeric(nbh_df['Positive7Day'])
    nbh_df = nbh_df.sort_values(by=['Positive7Day'], ascending = False)\
    .reset_index(drop = True)
    nbh_df.columns = ['DateStr', 'Neighbourhood', 'Weekly Positive']
    nbh_df['Date'] = nbh_df['DateStr'].apply(lambda x: pd.to_datetime(str(x),\
     format='%Y%m%d'))
    nbh_df = nbh_df.drop('DateStr', axis = 1)
    return nbh_df.iloc[:10,:]

#Daily Cases by Local Authority
def top_la_daily():
    '''
    Returns Local Authority new Covid case numbers
    '''

    day = latest_date(by_hb_id)
    sql_hb = f'''
    SELECT "Date", "CAName", "DailyPositive"
    FROM "{by_hb_id}"
    WHERE "Date" = {day}
    '''
    hb_df = get_api(by_hb_id, sql_hb)
    hb_df['DailyPositive'] = pd.to_numeric(hb_df['DailyPositive'])
    hb_df = hb_df.sort_values(by=['DailyPositive'], ascending = False)\
    .reset_index(drop = True)
    hb_df.columns = ['DateStr','Daily Positive', 'Local Authority']
    hb_df['Date'] = hb_df['DateStr'].apply(lambda x: pd.to_datetime(str(x),\
     format='%Y%m%d'))
    return hb_df.drop('DateStr', axis = 1)


def snap_shot(n_days):
    '''
    Returns a snap shot of  case numbers in Local Authority over time
    '''
    day = latest_date(by_hb_id)
    n_days = 5
    _n_days = month_before(by_hb_id, n_days)

    sql_hb_m = f'''
    SELECT "Date", "CAName", "PositivePercentage"
    FROM "{by_hb_id}"
    WHERE "Date" BETWEEN {_n_days} AND {day}
    ORDER BY "Date" DESC
    '''
    hb_m_df = get_api(by_hb_id, sql_hb_m)
    hb_m_df['PositivePercentage'] = pd.to_numeric(hb_m_df['PositivePercentage'])
    hb_m_df.columns = ['DateStr', 'PositivePercentage', 'Local Authority']
    hb_m_df['Date'] = hb_m_df['DateStr'].apply(lambda x: pd.to_datetime(str(x),\
     format='%Y%m%d'))
    hb_m_df = hb_m_df.drop('DateStr', axis = 1)
    return hb_m_df

def deaths():
    '''
    returns most recent daily covid related deaths
    from the Scottish Goverment
    '''
    sql_deaths = f'''
    SELECT "WeekEnding", "Deaths"
    FROM "{deaths_id}"
    ORDER BY "WeekEnding" ASC
    '''
    death_df = get_api(deaths_id, sql_deaths)
    death_df.columns = ['Deaths', 'Date']
    death_df['Date'] = death_df['Date'].apply(lambda x: pd.to_datetime(str(x),\
        format='%Y%m%d'))
    death_df['AvgDeaths'] = death_df['Deaths'].rolling(14,\
        win_type='triang', min_periods=1).mean()
    return death_df

#Creates Figures
def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    #New Covic cases over time for Scotland
    df_one = daily()
    df_one = df_one.set_index('Date').stack().reset_index()

    df_one.columns = ['Date', 'casetype', 'Cases']
    df_one = df_one.iloc[-100:,:]
    graph_one = []
    ct_list = df_one.casetype.unique().tolist()


    for ct in ct_list:
      x_val = df_one[df_one.casetype == ct]['Date'].tolist()
      y_val = df_one[df_one.casetype == ct]['Cases'].tolist()

      graph_one.append(go.Scatter(
              x = x_val,
              y = y_val,
              mode = 'lines',
              name = ct
              ),
          )
    layout_one = dict(title = 'Daily COVID-19 Cases in Scotland',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'New Cases'),
                font=dict( color="black"
                        )
                )


    #Top ten table of highest weekly covid Neighbourhoods
    df_two = top_nbh_daily()
    df_two = df_two.drop(['Date'], axis= 1)

    colors = n_colors('rgb(200, 0, 0)', 'rgb(255, 200, 200)',  10, colortype='rgb')
    df_two['c'] = colors
    graph_two = []
    graph_two.append(go.Table(
    header=dict(
        values=["<b>Neighbourhood<b>", "<b>Weekly Positive<b>"],
        line_color='darkslategrey', fill_color='white',
        align='center',
        font=dict(color='black', size=12)
  ),
    cells=dict(values=[df_two['Neighbourhood'], df_two['Weekly Positive']],
        line_color=[df_two['c']],
        fill_color=[df_two['c']],
        align='left',
        font=dict(color='white', size=12)
           )
        )
        )

    #New Daily Cases by Local Authority
    df_three = top_la_daily()
    df_three_s = df_three.sort_values(by = 'Daily Positive')
    graph_three = []

    hb_list = df_three_s['Local Authority'].tolist()
    for hb in hb_list:
      x_val = df_three_s[df_three_s['Local Authority'] == hb]['Local Authority'].tolist()
      y_val = df_three_s[df_three_s['Local Authority'] == hb]['Daily Positive'].tolist()
      graph_three.append(go.Bar(y = x_val,x = y_val, name = hb,orientation='h'))

    layout_three = dict(
                title = 'Daily Cases',
                xaxis = dict(
                            title = 'New Cases'
                            ),
                yaxis = dict(
                            autotick=False
                            ),
                autosize=False,
                width=500,
                height=900,
                showlegend = False,
                color = "y_val",
                margin=dict(
                            l=150,r=50,b=50,t=75,pad=4
                        )
                    )


    n_days = 10
    df_four = snap_shot(n_days)
    graph_four = []

    for hb in top_five:
      x_val = df_four[df_four['Local Authority'] == hb]['Date'].tolist()
      y_val = df_four[df_four['Local Authority'] == hb]['PositivePercentage'].tolist()

      graph_four.append(go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = hb,
                )
            )

    layout_four = dict(title = 'Percent of Tests Positive',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'Positive Test Percent(%)'),
                )


    top_five = df_three['Local Authority'].iloc[0:5].tolist()
    top_five_data = df_three.iloc[0:5,:]

    everyone = df_three.iloc[:,0].sum()
    top_5_tot = top_five_data.iloc[:,0].sum()
    other = everyone - top_5_tot
    other_date = top_five_data['Date'].iloc[0]
    other_data = {'Daily Positive':[other],'Local Authority':'Other', 'Date':other_date}
    other_pds = pd.DataFrame(data = other_data)
    top_five_data = pd.concat([top_five_data, other_pds])
    graph_five = []

    xlabels = top_five_data['Local Authority'].tolist()

    y_vals = top_five_data['Daily Positive'].tolist()
    graph_five.append(go.Pie(
                labels = xlabels,
                values = y_vals)
                )

    layout_five = dict(
                title={
        'text': 'Share of New Cases',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


    df_six = df_six.set_index('Date').stack().reset_index()

    df_six.columns = ['Date', 'casetype', 'Deaths']
    df_six = df_six.iloc[-100:,:]
    graph_six = []
    ct_list = df_six.casetype.unique().tolist()


    for ct in ct_list:
      x_val = df_six[df_six.casetype == ct]['Date'].tolist()
      y_val = df_six[df_six.casetype == ct]['Deaths'].tolist()

      graph_six.append(go.Scatter(
              x = x_val,
              y = y_val,
              mode = 'lines',
              name = ct
              ),
          )
    layout_six = dict(title = 'Weekly COVID-19 Deaths in Scotland',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'Deaths'),
                font=dict( color="black"
                        )
                )





    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures
