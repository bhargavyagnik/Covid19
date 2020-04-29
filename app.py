from flask import Flask,render_template
import pandas as pd


def get_world_data():
    world_data = pd.read_csv('stats/world_cases.csv')
    world_today = world_data.tail(1)
    total_cases=world_today['total_cases'].values[0]
    deaths=world_today['total_deaths'].values[0]
    new_today=world_today['new_cases'].values[0]
    new_deaths = world_today['new_deaths'].values[0]
    india=pd.read_csv("stats/case_time_series.csv")
    day=india.iloc[-1]
    total_cases_ind=day.values[2]
    new_today_ind=day.values[1]
    deaths_ind=day.values[6]
    new_deaths_ind=day.values[5]
    recover_ind=day.values[4]
    recover_ind_new=day.values[3]
    active_cases_ind=total_cases_ind-deaths_ind-recover_ind
    data = {"Total":total_cases ,
            "Deaths":deaths,
            "New":new_today,
            "new_deaths":new_deaths,
            'indtot':total_cases_ind,
            'indnew':new_today_ind,
            'inddea':deaths_ind,
            'indnewd':new_deaths_ind,
            'recind':recover_ind,
            'newrec':recover_ind_new,
            'indact':active_cases_ind
            }
    return data

def get_guj_data():
    guj=pd.read_csv('stats/state_wise.csv')
    gujj = pd.read_csv('stats/state_wise_daily.csv')
    guj=guj[guj['State']=="Gujarat"]
    data={"total":guj['Confirmed'].values[0],
          "recovered":guj['Recovered'].values[0],
          'deaths':guj['Deaths'].values[0],
          'active': guj['Active'].values[0],
          'newtot':gujj['GJ'].tail(3).values[0],
          'newrec':gujj['GJ'].tail(3).values[1],
          'newdeath':gujj['GJ'].tail(3).values[2]}
    return data

app = Flask(__name__)


@app.route('/' , methods=("POST", "GET"))
def home():
    data=get_world_data()
    ind_top10 = pd.read_csv('stats/state_wise.csv')
    ind_top10 = ind_top10.drop('State_code',axis=1)
    ind_top10 = ind_top10.head(11)
    return render_template('index.html',data=data,column_names=ind_top10.columns.values, row_data=list(ind_top10.values.tolist()),zip=zip)

@app.route('/Gujarat')
def Gujarat():
    data_guj=get_guj_data()
    return render_template('gujarat.html',data=data_guj)

@app.route('/World')
def World():
    return render_template('world.html')

@app.route('/Precaution')
def Precaution():
    return render_template('precaution.html')

@app.route('/Prediction')
def prediction():
    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(debug=True)
