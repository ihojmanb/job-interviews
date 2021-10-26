import json
import random
from datetime import timedelta, date

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def date_list_generator(start_dt, end_dt):
	list_of_dates= []
	for dt in daterange(start_dt, end_dt):
    		list_of_dates.append(dt.strftime("%Y-%m-%d"))
	return list_of_dates

start_dt = date(2019, 1, 1)
end_dt = date(2020, 12, 31)
dates_list = date_list_generator(start_dt, end_dt)
print(dates_list)

data = open("fake_data.json")
data = json.load(data)

with open("fake_data.json", "r") as fake_data:
	data = json.load(fake_data)


for stock in data:
	stock["prices"] = {}
	for date in dates_list:
		stock["prices"][date] = random.randint(1, 10) 

with open("fake_data.json", "w") as updated_fake_data:
        data = json.dump(data, updated_fake_data)

