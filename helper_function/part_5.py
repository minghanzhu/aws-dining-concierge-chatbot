import requests
import pprint
import json
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

URL = "https://api.yelp.com/v3/businesses/search"
location = "manhattan"
cuisine_type = "spanish"
aws_access_key_id = ""
aws_secret_access_key = ""

offset = 0
HEADERS = {"Authorization": "Bearer "
                            ""}


def add_restaurants(table, l_d):
    '''add new items to the table using DynamoDB.Table.put_item()'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

    # convert empty strings into None
    for d in l_d:
        for key, value in d.items():
            if value == "":
                d[key] = None

    for d in l_d:
        print(d["id"])
        table.put_item(
            Item={
                "id": d["id"],
                "name": d["name"],
                "address": d["address"],
                "coordinates": str(d["coordinates"]),
                "review_count": d["review_count"],
                "rating": str(d["rating"]),
                "zip_code": d["zip_code"],
                "cuisine_type": cuisine_type,
                "insertedAtTimestamp": str(datetime.datetime.now()),
            }
        )


def get_restaurant_by_id(table, id: str):
    '''retrieve the object using DynamoDB.Table.get_item()'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

    response = table.query(KeyConditionExpression=Key('id').eq(id))
    item = response['Items']
    pp = pprint.PrettyPrinter()
    pp.pprint(item)
    return item[0]


if __name__ == '__main__':
    '''Yelp API'''
    # l_d = []
    # for offset in range(0, 1000, 50):
    #     PARAMS = {'location': location, "term": cuisine_type, "limit": 50, "offset": offset}
    #
    #     r = requests.get(URL, params=PARAMS, headers=HEADERS)
    #     data = r.json()["businesses"]
    #     # pp = pprint.PrettyPrinter()
    #     # pp.pprint(data)
    #
    #     for d in data:
    #         # Requirements: Business ID, Name, Address, Coordinates, Number of Reviews, Rating, Zip Code
    #         dict_record = {
    #             "id": d["id"],
    #             "name": d["name"],
    #             "address": d["location"]["address1"],
    #             "coordinates": d["coordinates"],
    #             "review_count": d["review_count"],
    #             "rating": d["rating"],
    #             "zip_code": d["location"]["zip_code"],
    #             "cuisine_type": cuisine_type
    #         }
    #         l_d.append(dict_record)
    #
    # for d in l_d:
    #     print(d)
    #
    # j_d = json.dumps(l_d)
    #
    # with open("yelp-restaurants-" + cuisine_type + ".json", 'w') as out:
    #     json.dump(j_d, out)

    '''
    Get the DynamoDB service resource and the table
    '''

    import boto3

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # dynamodb = boto3.resource('dynamodb')
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurants')

    '''
    Store the restaurant records scraped into the table
    '''
    # with open(r"yelp-restaurants-" + cuisine_type + ".json", "r") as read:
    #     l_d = json.load(read)
    # l_d = json.loads(l_d)
    # add_restaurants(table, l_d)

    '''
    Use the DynamoDB table “yelp-restaurants” to fetch more information about the restaurants (restaurant name, 
    address, etc.)
    '''
    get_restaurant_by_id(table, "tguMh2GgOcU9fu6WN3dqpw")
