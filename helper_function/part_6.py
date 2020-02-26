from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import json
import random
import requests
import pprint


def add_restaurants_to_index(es, index, l_d):
    '''
    Store partial information for each restaurant scraped in ElasticSearch under the “restaurants” index, where each
    entry has a “Restaurant” data type. This data type will be of composite type stored as JSON in ElasticSearch.
    '''
    # https://elasticsearch-py.readthedocs.io/en/master/
    for d in l_d:
        d = {
            "RestaurantID": d["id"],
            "Cuisine": d["cuisine_type"],
        }
        print(d)
        # Create an ElasticSearch type under the index “restaurants” called “Restaurant”
        es.index(index=index, doc_type="Restaurant", body=d)


# def get_restaurant_by_cuisine_type(es, index, cuisine_type):
#     res = es.search(index=index, body={'query': {'match': {'Cuisine': cuisine_type}}})
#     # print("Got %d Hits:" % res['hits']['total']['value'])
#     # print(type(res['hits']['hits']))
#     # for hit in res['hits']['hits']:
#     #     print(hit)
#     # gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch and
#     # DynamoDB
#     random_restaurant = random.choice(res['hits']['hits'])
#     print(random_restaurant["_source"]["RestaurantID"])


def get_restaurant_by_cuisine_type(url, cuisine_type):
    r = requests.get(url + cuisine_type)
    l_d = r.json()["hits"]["hits"]
    random_restaurant = random.choice(l_d)
    # pp = pprint.PrettyPrinter()
    # pp.pprint(l_d)
    print(random_restaurant)
    random_restaurant_id = random_restaurant["_source"]["RestaurantID"]
    print(random_restaurant_id)
    return random_restaurant_id


if __name__ == '__main__':
    host = "search-yelp-restaurants-avoca2hrr5huzn3vyby2bf5lwm.us-east-2.es.amazonaws.com"  #
    region = "us-east-2"
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    cuisine_type = "spanish"

    with open(r"yelp-restaurants-" + cuisine_type + ".json", "r") as read:
        l_d = json.load(read)
    l_d = json.loads(l_d)

    # add_restaurants_to_index(es=es, index="restaurants", l_d=l_d)

    # get_restaurant_by_cuisine_type(es=es, index="restaurants", cuisine_type="chinese")
    get_restaurant_by_cuisine_type(
        url="https://search-yelp-restaurants-avoca2hrr5huzn3vyby2bf5lwm.us-east-2.es.amazonaws.com/restaurants"
            "/_search?q=Cuisine:",
        cuisine_type="chinese")

    # res = es.search(index="restaurants", body={"query": {"match_all": {}}})

    # res = es.search(index='restaurants', body={'query': {'match': {'Cuisine': 'chinese'}}})
    # print("Got %d Hits:" % res['hits']['total']['value'])
    # for hit in res['hits']['hits']:
    #     print(hit)
