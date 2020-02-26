import logging
import dateutil.parser
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def Greeting(message):
    return {
        "dialogAction": {
            "type": "ElicitIntent",
            "message": {
                "contentType": "PlainText",
                "content": "Hi there, how can I help you?"
            }
        }
    }

def Thank_You(message):
    return {
        "dialogAction": {
            "fulfillmentState": 'Fulfilled',
            "type": "Close",
            "message": {
                "contentType": "PlainText",
                "content": "You are welcome! See you next time!"
            }
        }
    }



def Dining_Suggestions(intent_request):
    if intent_request['invocationSource'] == 'DialogCodeHook':
        return {
            "dialogAction": {
                # "fulfillmentState": 'Fulfilled',
                "type": "ElicitSlot",
                "slots": intent_request['currentIntent']['slots']

            }
            }

    elif intent_request['invocationSource'] == 'FulfillmentCodeHook':
        sqs = boto3.client('sqs',
          aws_access_key_id = '',
          aws_secret_access_key = '')

        sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/447013652281/queue",
            DelaySeconds=1,
            MessageBody=(
                json.dumps(intent_request['currentIntent']['slots'])
            )

        )


        return {
            "dialogAction": {
                # "fulfillmentState": 'Fulfilled',
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": "Thanks, I have placed your reservation. Expect my recommendations shortly! Have a good day."
                }
            }
            }


def lambda_handler(event, context):

    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    intent_name = event['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'GreetingIntent':
        return Greeting(event)
    elif intent_name == "ThankYouIntent":
        return Thank_You(event)
    elif intent_name == "DiningSuggestionsIntent":
        return Dining_Suggestions(event)

    raise Exception('Intent with name ' + intent_name + ' not supported')
