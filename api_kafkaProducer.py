import requests
from kafka import KafkaProducer
import json
import time
import sys


def api_Producer():
    try:
        response = requests.get("https://randomuser.me/api/?results=1")
        response.raise_for_status()  # Raise an exception if the request fails

        random_data = response.json()["results"][0]
        
        data = {}

        data["full_name"] = f"{random_data['name'].get('title', '')}. {random_data['name'].get('first', '')} {random_data['name'].get('last', '')}"

        data["gender"] = random_data.get("gender", '')

        data["location"] = f"{random_data['location']['street'].get('number', '')}, {random_data['location']['street'].get('name', '')}"

        data["city"] = random_data['location'].get('city', '')

        data["country"] = random_data['location'].get('country', '')

        data["postcode"] = int(random_data['location'].get('postcode', 0))

        data["latitude"] = float(random_data['location']
                                ['coordinates'].get('latitude', 0.0))
        
        data["longitude"] = float(random_data['location']
                                ['coordinates'].get('longitude', 0.0))
        
        data["email"] = random_data.get("email", '')


        producer = KafkaProducer(
            bootstrap_servers=['kafka_broker_1:19092',
                               'kafka_broker_2:19093', 'kafka_broker_3:19094'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        current_time = time.time()
        while True:
            if time.time() > current_time + 60:
                break
            else:
                producer.send("json_data",  json.dumps(data).encode('utf-8'))
                time.sleep(10)  # Add a delay between sending messages

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    api_Producer()

    
