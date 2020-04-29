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
       'world':'static/world_map.svg'
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
    line_chart = pygal.Line(fill=True,show_legend=False,show_x_labels=False, show_y_labels=True, style=DefaultStyle)
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
    line_chart = pygal.Line(fill=True,show_legend=False, show_x_labels=False, show_y_labels=False, style=DefaultStyle)
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

if __name__=='__main__':
    raw_data=pd.read_csv('stats/raw_data.csv')
    state_wise=pd.read_csv('stats/state_wise.csv')
    state_wise_daily=pd.read_csv('stats/state_wise_daily.csv')
    statewise_tested_numbers_data=pd.read_csv('stats/statewise_tested_numbers_data.csv')
    case_time_series=pd.read_csv('stats/case_time_series.csv')
    tested_numbers_icmr_data=pd.read_csv('stats/tested_numbers_icmr_data.csv')
    world_cases=pd.read_csv('stats/world_cases.csv')
    world_cases_all=pd.read_csv('stats/world_all_cases.csv')
    plot_cases_worldwide(world_cases,paths['cw'])
    cases,deaths,recovered=plot_cases_india(case_time_series,paths['ci'])
    plot_prediction_india(cases,deaths,paths['pr'])
    #testing_findings(statewise_tested_numbers_data,state_wise,paths['ttpos'])
    plot_male_female(raw_data,paths['mf'])
    plot_world_map(world_cases_all,paths['world'])

