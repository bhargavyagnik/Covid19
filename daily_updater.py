import pandas as pd
import pygal
from pygal.style import DefaultStyle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from iso3166 import countries
from pygal.style import RotateStyle


paths={'cw':'static/cases_worldwide.svg',
       'ci':'static/cases_india.svg',
       'pr':'static/prediction_india.svg',
       'ttpos':'static/test_to_positive_stacked.svg',
       'mf':'static/male_female.svg',
       'sttst':'static/state_wise_testing_radar.svg',
       'world':'static/world_map.svg',
       'guj':'static/guj.svg',
        'guj2':'static/guj2.svg',
       'ic':'static/ind_cases.svg',
       'ir':'static/ind_recovered.svg',
       'id':'static/ind_dead.svg',
       'piei':'static/piechart_india.svg',
       'pieg':'static/piechart_guj.svg'
       }

def plot_cases_worldwide(df,path):
    start_date = df.head(1).date.values[0]
    end_date = df.tail(1).date.values[0]
    daterange = pd.date_range(start_date, end_date)
    dates = []
    cases = []
    deaths =  []
    for single_date in daterange:
        d = single_date.strftime("%Y-%m-%d")
        dates.append(d)
        temp = df[df['date'] == d]

        case = temp['total_cases'].values[0]
        death = temp['total_deaths'].values[0]
        cases.append(case)
        deaths.append(death)
    line_chart = pygal.Line(fill=True,show_legend=True,show_x_labels=True, show_y_labels=True, style=DefaultStyle)
    line_chart.add('Cases', cases, show_dots=True,dots_size=8)
    line_chart.add('Deaths', deaths, show_dots=True,dots_size=8)
    line_chart.x_labels = map(str, dates)
    line_chart.render_to_file(path)

def plot_cases_india(df,path):
    dates = []
    cases = []
    deaths = []
    recovered=[]
    for i in range(len(df)):
        dates.append(df.iloc[i].values[0])
        cases.append(df.iloc[i].values[2])
        deaths.append(df.iloc[i].values[6])
        recovered.append(df.iloc[i].values[4])
    line_chart = pygal.Line(fill=True,show_legend=True, show_x_labels=True, show_y_labels=False, style=DefaultStyle)
    line_chart.add('Cases', cases, show_dots=True,dots_size=8)
    line_chart.add('Recovered', recovered, show_dots=True,dots_size=8)
    line_chart.add('Deaths', deaths, show_dots=True,dots_size=8)
    line_chart.x_labels = map(str, dates)
    line_chart.render_to_file(path)
    return cases,deaths,recovered

def plot_prediction_india(cases,deaths,path):
    dates=[i+1 for i in range(len(cases))]
    X = np.array(dates[-10:])
    Y = np.log(cases[-10:])
    Z = np.log(deaths[-10:])
    X = X[:, np.newaxis]
    lin_reg_cases= LinearRegression()
    lin_reg_cases.fit(X, Y)
    lin_reg_deaths = LinearRegression()
    lin_reg_deaths.fit(X, Z)
    line_chart = pygal.Line(fill=False, show_legend=False, show_x_labels=True, show_y_labels=False, style=DefaultStyle)
    line_chart.x_labels = map(str, ['Yesterday','Today','Tommorow','Day-After'])
    line_chart.add('Cases',[np.exp(lin_reg_cases.predict([[dates[-2]]])[0]),
                            np.exp(lin_reg_cases.predict([[dates[-1]]])[0]),
                            np.exp(lin_reg_cases.predict([[dates[-1]+1]])[0]),
                            np.exp(lin_reg_cases.predict([[dates[-1]+2]])[0])],show_dots=True,dots_size=15)
    line_chart.add('Deaths',
                   [np.exp(lin_reg_deaths.predict([[dates[-2]]])[0]),
                    np.exp(lin_reg_deaths.predict([[dates[-1]]])[0]),
                    np.exp(lin_reg_deaths.predict([[dates[-1] + 1]])[0]),
                    np.exp(lin_reg_deaths.predict([[dates[-1] + 2]])[0])], show_dots=True,dots_size=15)
    line_chart.render_to_file(path)

def testing_findings(df,df2,path):
    tests = []
    cases = []
    states = []
    for state in df.State.unique():
        temp = df[df['State'] == state]
        if len(temp)>2:
            if temp.tail(1).isnull().values[0][2]:
                temp = temp.iloc[-2]
            else:
                temp = temp.iloc[-1]
            states.append(state)
            tests.append(temp.values[2])
            cases.append(temp.values[3])
    ratio=[]
    for i in range(len(cases)):
        if tests[i] != np.nan and cases[i] !=np.nan:
            ratio.append(int(100*tests[i]/cases[i]))
    line_chart = pygal.Bar()
    line_chart.title = 'Statewise calculation'
    line_chart.x_labels = map(str, states)
    line_chart.add('Test',tests)
    line_chart.add('Cases',cases)
    line_chart.add('Test Positive Per 100',ratio)
    line_chart.render_table(style=True)

def plot_male_female(df,path):
    g=df.Gender.value_counts()
    Male=g.values[0]
    Female = g.values[1]
    tot=Male+Female
    Male=100*Male/tot
    Female=100*Female/tot
    pie_chart = pygal.Pie(inner_radius=.4)
    pie_chart.title = 'Male vs Female affected becaues of COVID-19'
    pie_chart.add('Male', Male)
    pie_chart.add('Female', Female)
    pie_chart.render_to_file(path)

def plot_world_map(df,path):
    world_dict={}
    for c in countries:
        try:
            world_dict[str(c.alpha2).lower()]=df[df['iso_code'] ==str(c.alpha3).upper()].iloc[-1][3]
        except:
            world_dict[str(c.alpha2).lower()]=0
    worldmap_chart = pygal.maps.world.World(style=RotateStyle('#336699'))
    worldmap_chart.force_uri_protocol = "http"
    worldmap_chart.value_formatter = lambda x: "{:,}".format(x)
    worldmap_chart.value_formatter = lambda y: "{:,}".format(y)
    worldmap_chart.title = 'Covid 19 stats'
    worldmap_chart.add('COVID-19', world_dict)
    worldmap_chart.render_to_file(path)

def plot_guj_1(df):
    t=df['Detected District'].value_counts()[:10]
    line_chart = pygal.HorizontalBar()
    line_chart.title = 'Cities with Highest Cases'
    for i in range(len(t)):
        line_chart.add(t.index[i],t[i])
    line_chart.render_to_file(paths['guj'])

def plot_cases_rec_ded_state(df,ttt):
    daterange = pd.date_range(df.Date[0], df.iloc[-1].values[0])
    line_chart1 = pygal.Line()
    line_chart2 = pygal.Line()
    line_chart3 = pygal.Line()
    line_chart3.title = 'Recovered'
    line_chart2.title = 'Deaths'
    line_chart1.title = 'Cases'
    line_chart4 = pygal.Line(fill=True)
    line_chart4.title = 'Gujarat COVID-19'
    ttt = pd.read_csv('stats/state_wise.csv')
    for i in range(len(df.columns) - 3):
        dates = []
        cases = []
        recovered = []
        deaths = []
        state = df.columns[3 + i]
        for single_date in daterange:
            d = single_date.strftime("%d-%b-%y")
            dates.append(d)
            temp = df[df['Date'] == d]
            case = temp[state].values[0]
            death = temp[state].values[2]
            rec = temp[state].values[1]
            cases.append(case)
            deaths.append(death)
            recovered.append(rec)
        line_chart3.add(ttt[ttt['State_code'] == state]['State'].values[0], recovered, dots_size=1)
        line_chart2.add(ttt[ttt['State_code'] == state]['State'].values[0], deaths, dots_size=1)
        line_chart1.add(ttt[ttt['State_code'] == state]['State'].values[0], cases, dots_size=1)
        line_chart1.x_labels = map(str, dates)
        line_chart2.x_labels = map(str, dates)
        line_chart3.x_labels = map(str, dates)
        if (state == 'GJ'):
            line_chart4.add("Cases", cases)
            line_chart4.add("Recovered", recovered)
            line_chart4.add("Deaths", deaths)
            line_chart4.x_labels = map(str, dates)
    line_chart1.render_to_file(paths['ic'])
    line_chart2.render_to_file(paths['id'])
    line_chart3.render_to_file(paths['ir'])
    line_chart4.render_to_file(paths['guj2'])

def plot_spread_pie(df,df_guj):
    t=df['Type of transmission'].value_counts()
    pie_chart = pygal.Pie()
    pie_chart.title = 'Transmission type (TBD-To Be Decided)*(for Available data)'
    pie_chart.add(t.index[0], t[0])
    pie_chart.add(t.index[1], t[1])
    pie_chart.add(t.index[2], t[2])
    pie_chart.render_to_file(paths['piei'])
    t = df_guj['Type of transmission'].value_counts()
    pie_chart = pygal.Pie()
    pie_chart.title = 'Transmission type (TBD-To Be Decided)*(for Available data)'
    pie_chart.add(t.index[0], t[0])
    pie_chart.add(t.index[1], t[1])
    pie_chart.add(t.index[2], t[2])
    pie_chart.render_to_file(paths['pieg'])




if __name__=='__main__':
    raw_data=pd.read_csv('stats/raw_data.csv')
    state_wise=pd.read_csv('stats/state_wise.csv')
    state_wise_daily=pd.read_csv('stats/state_wise_daily.csv')
    statewise_tested_numbers_data=pd.read_csv('stats/statewise_tested_numbers_data.csv')
    case_time_series=pd.read_csv('stats/case_time_series.csv')
    tested_numbers_icmr_data=pd.read_csv('stats/tested_numbers_icmr_data.csv')
    world_cases=pd.read_csv('stats/world_cases.csv')
    world_cases_all=pd.read_csv('stats/world_all_cases.csv')
    guj=pd.read_csv('stats/gujarat.csv')
    plot_cases_worldwide(world_cases,paths['cw'])
    cases,deaths,recovered=plot_cases_india(case_time_series,paths['ci'])
    plot_prediction_india(cases,deaths,paths['pr'])
    #testing_findings(statewise_tested_numbers_data,state_wise,paths['ttpos'])
    plot_male_female(raw_data,paths['mf'])
    plot_world_map(world_cases_all,paths['world'])
    plot_guj_1(guj)
    plot_cases_rec_ded_state(state_wise_daily,state_wise)
    plot_spread_pie(raw_data,guj)


