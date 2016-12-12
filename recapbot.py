from itty import *
from process_messages import process
import urllib2
import requests
import json

#Gets messages (default number: 1000 messages) from a chat room:
def getMessages(room_id, maxNo):
    try:
        #GET request for obtaining all messages in a specific Spark room:
        response = requests.get(
            url="https://api.ciscospark.com/v1/messages/?roomId=" + room_id + "&max="+maxNo,
            headers={
                "Authorization": "Bearer " +bearer,
                "Content-Type": "application/json; charset=utf-8",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    return response.content

#Gets the maximum number of messages to filter from user input, if "/max" specified (default: 1000 messages):
def getMaxNoMessages(parameters):
    maxNo = str(1000)
    if '/max' in parameters:
        for ch in [' ', '/max', '@']:
            if ch in parameters:
                parameters = parameters.replace(ch, '')
        if parameters.isdigit():
            maxNo = str(parameters)
    return maxNo

#Messages returned to the user if an unknown command is issued or if help is required:
def getHelpMessage():
    title = "**RecapBot:** This bot filters the messages in the current room where the bot is called and outputs all important messages in a larger font."
    options = "The bot currently has the following functionalities:"
    option1 = "1. *'@recapbot'* - filters all messages within the room"
    option2 = "2. *'@recapbot /max X'* - filters X number of messages within the room"
    github = "\r\nCheck out the [github page](https://github.com/Jay-Plumb/hackathon-chat) for more information."

    message = "\n".join([title, options, option1, option2, github])
    return message

def getErrorMessage():
    msg = "You entered an invalid command!"
    newLine = ""
    helpMsg = getHelpMessage()
    return '\r\n'.join([msg, newLine, helpMsg])

def sendSparkGET(message_id):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
    """
    request = requests.get(
        url="https://api.ciscospark.com/v1/messages/" + message_id,
        headers={
            "Authorization": "Bearer " +bearer,
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    return request.content

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
    using the sendSparkGET() function.  The message text is parsed.

    """
    webhook = json.loads(request.body)

    initMess = sendSparkGET(webhook["data"]["id"])
    initMess = json.loads(initMess)

    #The following lines are not called if webhook was triggered by bot:
    if webhook["data"]["personEmail"] != bot_email:
        parameters = initMess.get('text', '').lower()
        if bot_name in parameters:
            #Remove bot name from message:
            parameters = parameters.replace(bot_name, '')

            if ("/max" in parameters or not parameters.strip()):
                #Default number of messages is 1000, unless specified by user through '/max':
                maxNo = getMaxNoMessages(parameters)

                #Get all messages in room:
                result = getMessages(webhook['data']['roomId'], maxNo)

                data = []
                result = json.loads(result)
                filtered_data = {"items": data}

                #'For' loop to filter out all messages outputted by the bot and that call the bot:
                for item in result["items"]:
                    if (item['personEmail'] != bot_email):
                        if (bot_name not in item['text']):
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
                # with open('processed.json', 'w') as outfile:
                #     json.dump(messages, outfile, sort_keys=True, indent=4, separators=(',', ': '))

            #If the user asks for 'help', the bot outputs a message with its functionalities:
            elif "/help" in parameters:
                sendSparkPOST("https://api.ciscospark.com/v1/messages/", {"roomId": webhook['data']['roomId'], "markdown": getHelpMessage()})
            #If an unknown command is given, the bot returns the help message:
            else:
                sendSparkPOST("https://api.ciscospark.com/v1/messages/", {"roomId": webhook['data']['roomId'], "markdown": getErrorMessage()})

    return "true"

####Values of the bot#####
bot_email = "recapbot@gmail.com"
bot_name = "recapbot"
bearer = "OGM2MjljMzMtZTZiYS00YTc2LWJmOTUtZGFjNWY0YmZkZDUwZTlkNTg2N2QtNWUy"
run_itty(server='wsgiref', host='127.0.0.1', port=8080)