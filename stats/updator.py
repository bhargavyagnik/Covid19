import pandas as pd
import io
import requests


def get_data(url):
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')))

def update():
    raw_data= get_data('https://api.covid19india.org/csv/latest/raw_data1.csv')
    raw_data2 = get_data('https://api.covid19india.org/csv/latest/raw_data2.csv')
    raw_data3= get_data('https://api.covid19india.org/csv/latest/raw_data3.csv')
    raw_data=raw_data.append(raw_data2)
    raw_data = raw_data.append(raw_data3)
    state_wise = get_data("https://api.covid19india.org/csv/latest/state_wise.csv")
    state_wise_daily = get_data("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
    statewise_tested_numbers_data=get_data('https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv')
    case_time_series = get_data('https://api.covid19india.org/csv/latest/case_time_series.csv')
    tested_numbers_icmr_data = get_data('https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv')
    world_cases = get_data("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    world_case = world_cases[world_cases['location'] == "World"]
    state_wise = state_wise[['State', 'Confirmed', 'Recovered', 'Deaths', 'Active', 'State_code']]
    raw_data.to_csv('raw_data.csv',index=False)
    state_wise.to_csv('state_wise.csv', index=False)
    state_wise_daily.to_csv('state_wise_daily.csv', index=False)
    statewise_tested_numbers_data.to_csv('statewise_tested_numbers_data.csv', index=False)
    case_time_series.to_csv('case_time_series.csv', index=False)
    tested_numbers_icmr_data.to_csv('tested_numbers_icmr_data.csv', index=False)
    world_case.to_csv('world_cases.csv',index=False)
    world_cases.to_csv('world_all_cases.csv',index=False)
    guj=raw_data[raw_data['Detected State']=='Gujarat']
    print(len(guj))
    guj.to_csv('gujarat.csv',index=False)


if __name__ == '__main__':
    update()

