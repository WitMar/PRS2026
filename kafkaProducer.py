import json
import time
from datetime import datetime
from json import dumps

import requests
import schedule
from kafka import KafkaProducer


def poll():
    schedule.every(5).minutes.do(lambda: job_air())
    schedule.every(60).minutes.do(lambda: job())
    while True:
        schedule.run_pending()
        print('ping')
        time.sleep(60 * 5)


def job():
    producer = KafkaProducer(bootstrap_servers='150.254.78.69:29092',
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.gios.gov.pl%2Fpjp-api%2Frest%2Fdata%2FgetData%2F6087&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=sL%2BcA1dXEC%2BLeDBtB0VAxlLu4%2BKVnR%2B6mvVsD5ECNR0%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')
    result = {}
    data = json.loads(my_json)
    result["SO2"] = data['values'][1]['value']
    result["date"] = data['values'][1]['date']

    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.gios.gov.pl%2Fpjp-api%2Frest%2Fdata%2FgetData%2F6085&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=m94hb%2FPG89%2FWURWgymF0iYyRd0XZSF5cIh40vNSywb4%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    result["PM10"] = data['values'][1]['value']

    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.gios.gov.pl%2Fpjp-api%2Frest%2Fdata%2FgetData%2F6074&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=8CjugPHPi7%2BaMfi0lEUCAJvrL6b1yaAkZJkHu%2FKy1%2FM%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    result["C6H6"] = data['values'][1]['value']

    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.gios.gov.pl%2Fpjp-api%2Frest%2Fdata%2FgetData%2F6076&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=72s3j50zyCgOngmsvNLB7xveULkRfcvbcr2OxjE4Jfs%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    result["CO"] = data['values'][1]['value']

    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.gios.gov.pl%2Fpjp-api%2Frest%2Fdata%2FgetData%2F6081&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=LhNJivYL3jhyqPV%2Bo4SHRC4XKqOhNAMLtEOk6SUs8H0%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    result["NO2"] = data['values'][1]['value']

    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.gios.gov.pl%2Fpjp-api%2Frest%2Fdata%2FgetData%2F6083&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=Kt9np64%2FqMMSehUp75E8qmMFxClbY3TtQvdaffcCnxA%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    result["O3"] = data['values'][1]['value']
    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.gios.gov.pl%2Fpjp-api%2Frest%2Fdata%2FgetData%2F20176&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=N7DZUxgG2UlEa8%2FA%2FNrjmLWZK8epKoDX5wx9O1PiJrY%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    result["PM2.5"] = data['values'][1]['value']

    print(data)
    producer.send('air_poznan_test', data)
    producer.flush()

    producer.close()


def job_air():
    producer = KafkaProducer(bootstrap_servers='150.254.78.69:29092',
                             value_serializer=lambda x: dumps(x).encode('utf-8'))
    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.openweathermap.org%2Fdata%2F2.5%2Fweather%3Flat%3D52.4064%26lon%3D16.9252%26appid%3Dec61953c03e99f1d34cac6b3852680f3%26units%3Dmetric&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=80fcg9WlZV2jS27IW7mPWWa83FCed5V0tIck%2B4ijWhc%3D&amp;reserved=0")

    my_json = response.content.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    result = {}
    result['temp'] = data['main']['temp']
    result['temp_feel'] = data['main']['temp']
    result['temp_min'] = data['main']['temp_min']
    result['temp_max'] = data['main']['temp_max']
    result['pressure'] = data['main']['pressure']
    result['humidity'] = data['main']['humidity']
    result['visibility'] = data['visibility']
    result['wind_speed'] = data['wind']['speed']
    result['sunrise'] = datetime.fromtimestamp(data['sys']['sunrise']).strftime("%m-%d-%Y %H:%M:%S")
    result['sunset'] = datetime.fromtimestamp(data['sys']['sunset']).strftime("%m-%d-%Y %H:%M:%S")

    print(data)
    producer.send('temp_poznan_test', data)
    producer.flush()

    response = requests.get(
        "https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fapi.coingecko.com%2Fapi%2Fv3%2Fexchange_rates&amp;data=05%7C01%7Cmw%40amu.edu.pl%7C24ece5853e2b48f5736d08da465ae6ec%7C73689ee1b42f4e25a5f666d1f29bc092%7C0%7C0%7C637899653478944227%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=kvH5jHBVXiNJcxcipEOjKfJcwy47WY78mXDip9apc9s%3D&amp;reserved=0")
    my_json = response.content.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    result = {}
    result['Bitcoin'] = 1.0
    result['eth'] = data['rates']['eth']['value']
    result['ltc'] = data['rates']['ltc']['value']
    result['usd'] = data['rates']['usd']['value']
    result['aud'] = data['rates']['aud']['value']
    result['cad'] = data['rates']['cad']['value']
    result['chf'] = data['rates']['chf']['value']
    result['eur'] = data['rates']['eur']['value']
    result['gbp'] = data['rates']['gbp']['value']
    result['pln'] = data['rates']['pln']['value']
    print(data)

    producer.send('bitcoin_test', data)
    producer.flush()

    producer.close()

def main():
    poll()

if __name__ == "__main__":
    main()
