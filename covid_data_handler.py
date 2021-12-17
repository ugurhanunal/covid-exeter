import sched
import time
import covid_logger
from uk_covid19 import Cov19API


def parse_csv_data(csv_filename):
    file = open(csv_filename, 'r')
    return [row for row in file]


def process_covid_csv_data(covid_csv_data):
    last7days_cases = 0
    total_deaths = 0
    for i in range(3, 10):
        last7days_cases += int(covid_csv_data[i].strip().split(',')[6])
    current_hospital_cases = int(covid_csv_data[1].strip().split(',')[5])
    for i in range(1, len(covid_csv_data)):
        cum_death = covid_csv_data[i].strip().split(',')[4]
        if len(cum_death) > 0:
            total_deaths = int(cum_death)
            break
    return last7days_cases, current_hospital_cases, total_deaths


def covid_API_request(location="Exeter", location_type="ltla"):
    loc = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }
    api = Cov19API(filters=loc, structure=cases_and_deaths)
    return api.get_json()


def schedule_covid_updates(update_interval, location="Exeter", location_type="ltla"):
    s = sched.scheduler(time.time, time.sleep)

    def update(sc):
        data = covid_API_request(location, location_type)
        covid_logger.log("covid_data: "+str(len(str(data)))+" byte")
        s.enter(update_interval, 1, update, (sc,))

    s.enter(0, 1, update, (s,))
    s.run()
