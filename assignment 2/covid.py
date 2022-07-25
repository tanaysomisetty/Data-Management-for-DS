import csv
import re

covid_rows = []
latlon = {}
city_occurs = {}
symptom_occurs = {}

# -------- Set Up --------
def read_csv(file):
    reader = csv.DictReader(open(file))

    with open(file) as csvfile:
        global covid_fieldnames
        covid_fieldnames = reader.fieldnames
        for row in reader:
            covid_rows.append(row)

# -------- # 2.1 --------
def replace_age_range():
    for row in covid_rows:
        age = row['age']
        res = re.search('^[0-9]+\-[0-9]+$', age)
        if res:
            lo,hi = age.split('-')
            lo = float(lo)
            hi = float(hi)
            avgAge = (lo+hi) / 2
            avgAge = round(avgAge)
            row['age'] = avgAge

# -------- # 2.2 --------
def change_date_format():
    for row in covid_rows:
        new_date_onset = change_date_onset(row['date_onset_symptoms'])
        new_date_admission = change_date_onset(row['date_admission_hospital'])
        new_date_confirmation = change_date_onset(row['date_confirmation'])
        row['date_onset_symptoms'] = new_date_onset
        row['date_admission_hospital'] = new_date_admission
        row['date_confirmation'] = new_date_confirmation

def change_date_onset(date):
    dd,mm,yy = date.split('.')
    new_date = mm + '.' + dd + '.' + yy
    return new_date

def change_date_admission(date):
    dd, mm, yy = date.split('.')
    new_date = mm + '.' + dd + '.' + yy
    return new_date

def change_date_confirmation(date):
    dd, mm, yy = date.split('.')
    new_date = mm + '.' + dd + '.' + yy
    return new_date

# -------- # 2.3 --------
def create_latlon_dict():
    for row in covid_rows:
        province = row['province']
        lat = row['latitude']
        lon = row['longitude']
        lat_list = []
        lon_list = []
        if province in latlon:
            lat_list = latlon[province][0]
            lon_list = latlon[province][1]
        if lat != 'NaN':
            lat_list.append(float(lat))
        if lon != 'NaN':
            lon_list.append(float(lon))
        latlon[province] = (lat_list, lon_list)

def fill_latlon():
    for row in covid_rows:
        province = row['province']
        if row['latitude'] == 'NaN':
            lat_list = latlon[province][0]
            avg_lat = sum(lat_list) / len(lat_list)
            avg_lat = round(avg_lat, 2)
            row['latitude'] = avg_lat
        if row['longitude'] == 'NaN':
            lon_list = latlon[province][1]
            avg_lon = sum(lon_list) / len(lon_list)
            avg_lon = round(avg_lon, 2)
            row['longitude'] = avg_lon

# -------- # 2.4 --------
def create_city_dict():
    for row in covid_rows:
        province = row['province']
        city = row['city']
        cities_in_prov = {}
        if province in city_occurs:
            cities_in_prov = city_occurs[province]
        if city != 'NaN':
            if city in cities_in_prov:
                city_count = cities_in_prov[city]
                cities_in_prov[city] = city_count + 1
            else:
                cities_in_prov[city] = 1
            city_occurs[province] = cities_in_prov

def fill_city():
    for row in covid_rows:
        province = row['province']
        city = row['city']
        if city == 'NaN':
            sorted_cities = sorted(city_occurs[province].items(), key=lambda x:x[1], reverse=True)
            row['city'] = sorted_cities[0][0]

# -------- # 2.5 --------
def create_symptom_dict():
    for row in covid_rows:
        province = row['province']
        symptoms = row['symptoms']
        if symptoms != 'NaN':
            symptoms_lst = symptoms.split(';')
            prov_dict = {}
            if province in symptom_occurs:
                prov_dict = symptom_occurs[province]
            for num,s in enumerate(symptoms_lst):
                s = s.strip()
                if s in prov_dict:
                    symp_count = prov_dict[s]
                    prov_dict[s] = symp_count + 1
                else:
                    prov_dict[s] = 1
            symptom_occurs[province] = prov_dict

def fill_symptom():
    for row in covid_rows:
        province = row['province']
        symptoms = row['symptoms']
        if symptoms == 'NaN':
            sorted_symps = sorted(symptom_occurs[province].items(), key=lambda x:x[1], reverse=True)
            row['symptoms'] = sorted_symps[0][0]



# -------- Output to CSV --------
def output(file):
    with open(file,'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=covid_fieldnames, delimiter=',')
        writer.writeheader()

        for row in covid_rows:
            writer.writerow(row)



# -------- main function --------
def main():
    read_csv('covidTrain.csv')
    replace_age_range()
    change_date_format()
    create_latlon_dict()
    fill_latlon()
    create_city_dict()
    fill_city()
    create_symptom_dict()
    fill_symptom()
    output('covidResult.csv')


main()