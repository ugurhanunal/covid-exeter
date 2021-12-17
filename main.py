from test_sample import *
import threading

test_parse_csv_data()
test_process_covid_csv_data()

threading.Thread(target=test_schedule_covid_updates).start()
threading.Thread(target=test_schedule_news).start()
