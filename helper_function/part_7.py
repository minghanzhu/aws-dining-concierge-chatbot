import boto3
import ast
import random
# from elasticsearch import Elasticsearch, RequestsHttpConnection
# from requests_aws4auth import AWS4Auth
import pprint
from boto3.dynamodb.conditions import Key, Attr

# https://stackoverflow.com/questions/50871512/curl-request-to-python-as-command-line
import requests


def get_restaurant_by_cuisine_type(url, cuisine_type):
    r = requests.get(url + cuisine_type)
    l_d = r.json()["hits"]["hits"]
    random_restaurant = random.choice(l_d)
    # pp = pprint.PrettyPrinter()
    # pp.pprint(l_d)
    # print(random_restaurant)
    random_restaurant_id = random_restaurant["_source"]["RestaurantID"]
    # print(random_restaurant_id)
    return random_restaurant_id


def get_restaurant_by_id(table, id: str):
    '''retrieve the object using DynamoDB.Table.get_item()'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

    response = table.query(KeyConditionExpression=Key('id').eq(id))
    item = response['Items']
    return item[0]


def make_sms(cuisine_type: str, people_num, time, restaurant_name, restaurant_location):
    sms = "Hello! Here are my " + cuisine_type.upper() + " restaurant suggestion for " + people_num + " people at " \
          + time + \
          ": " + restaurant_name + " at " + restaurant_location
    return sms

    # Send your sms message.
    # client.publish(
    #     PhoneNumber="+17817955652",
    #     Message="Hello World!"
    # )


if __name__ == '__main__':

    aws_access_key_id = ""
    aws_secret_access_key = ""

    '''
    SQS
    '''
    sqs = boto3.client('sqs',
                       aws_access_key_id='',
                       aws_secret_access_key='',
                       region_name="us-east-1")

    response = sqs.receive_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/447013652281/queue",
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    if "Messages" in response.keys():
        handler = response['Messages'][0]["ReceiptHandle"]

        sqs.delete_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/447013652281/queue",
            ReceiptHandle=handler
        )

        data = response['Messages'][0]["Body"]
        print(data)
        data = ast.literal_eval(data)

        cuisine_type = data["Cuisine"]
        phone_number = data["Phone_number"]
        people_num = data["Number_of_people"]
        time = data["Dining_Time"]
        location = data["Location"]

        print(cuisine_type, phone_number, people_num, time, location)

        '''
        Elasticsearch
        '''

        restaurant_id = get_restaurant_by_cuisine_type(
            url="https://search-yelp-restaurants-avoca2hrr5huzn3vyby2bf5lwm.us-east-2.es.amazonaws.com/restaurants"
                "/_search?q=Cuisine:",
            cuisine_type=cuisine_type)
        print(restaurant_id)

        '''
        DynamoDB
        '''
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        dynamodb = session.resource('dynamodb')
        table = dynamodb.Table('yelp-restaurants')

        restaurant = get_restaurant_by_id(table=table, id=restaurant_id)
        pp = pprint.PrettyPrinter()
        pp.pprint(restaurant)

        '''
        SNS
        '''
        ms = make_sms(cuisine_type, people_num, time, restaurant["name"], restaurant["address"])
        print(ms)

        # Send your sms message

        client = boto3.client(
            "sns",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            # https://docs.aws.amazon.com/sns/latest/dg/sns-supported-regions-countries.html
            region_name="us-east-1"
        )

        # client.publish(
        #     PhoneNumber="+1" + str(phone_number),
        #     Message=ms
        # )
