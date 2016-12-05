from itty import *
from process_messages import process
import urllib2
import requests
import json

#Gets messages (up to 1000 messages) from a chat room:
def getMessages(room_id):
    try:
        #GET request for obtaining all messages in a specific Spark room:
        response = requests.get(
            url="https://api.ciscospark.com/v1/messages/?roomId=" + room_id + "&max=1000",
            headers={
                "Authorization": "Bearer " +bearer,
                "Content-Type": "application/json; charset=utf-8",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    return response.content

def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                             headers={"Accept" : "application/json",
                                      "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.

    """
    webhook = json.loads(request.body)

    #The following lines are not called if webhook was triggered by bot:
    if webhook["data"]["personEmail"] != bot_email:
        result = getMessages(webhook['data']['roomId'])

        data = []
        result = json.loads(result)
        filtered_data = {"items": data}

        #'For' loop to filter out all messages outputted by the bot and that call the bot:
        for item in result["items"]:
            if (item['personEmail'] != bot_email):
                if (item['text'] != bot_name):
                    filtered_data["items"].append(item)
        #Convert dictionary of filtered data into a prettified JSON file:
        with open('unprocessed.json', 'w') as outfile:
            json.dump(filtered_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

        #Generate unique markdowns for the filtered messages and reverse their order, so that older messages are outputted first:
        messages = process('unprocessed.json')
        messages["items"].reverse()
        #POST request to output all markdown text onto the Spark room:
        for item in messages["items"]:
            sendSparkPOST("https://api.ciscospark.com/v1/messages/", {"roomId": webhook['data']['roomId'], "markdown": item["markdown"]})

        #Create a prettified JSON file for each message, storing the 'markdown' generated:
        with open('processed.json', 'w') as outfile:
            json.dump(messages, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    return "true"

####Values of the bot#####
bot_email = "recapbot@gmail.com"
bot_name = "recapbot"
bearer = "OGM2MjljMzMtZTZiYS00YTc2LWJmOTUtZGFjNWY0YmZkZDUwZTlkNTg2N2QtNWUy"
run_itty(server='wsgiref', host='127.0.0.1', port=8080)