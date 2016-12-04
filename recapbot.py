from itty import *
import urllib2
import requests
import json

def getMessages(room_id):
    print("ROOM:")
    try:
        response = requests.get(
            url="https://api.ciscospark.com/v1/messages/?roomId=" + room_id,
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


def sendSparkGET(message_id):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    # request = urllib2.Request('https://api.ciscospark.com/v1/messages/' + message_id,
    #                         headers={"Accept" : "application/json",
    #                                  "Content-Type":"application/json"})
    # request.add_header("Authorization", "Bearer "+bearer)
    # contents = urllib2.urlopen(request).read()
    try:
        response = requests.get(
            url="https://api.ciscospark.com/v1/messages/" + message_id,
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
    #print contents
    return contents



@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    /batman    - replies to the room with text
    /batcave   - echoes the incoming text to the room
    /batsignal - replies to the room with an image
    """
    webhook = json.loads(request.body)
    print "web"
    print webhook['data']['roomId']
    print webhook['data']['id']
    #print('https://api.ciscospark.com/v1/messages/')
    #print('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))

    #result = sendSparkGET(webhook['data']['id'])
    result = getMessages(webhook['data']['roomId'])
    # result = getMessages(webhook['data']['roomId'])
    result = json.loads(result)
    
    #print webhook['data']['roomId']
    #print result
    # msg = None
    # if webhook['data']['personEmail'] != bot_email:
    #     #json.loads(getMessages(webhook['data']['roomId']))
    #     print "TEST: \n" 
    #     print result
    #     in_message = result.get('text', '').lower()
    #     in_message = in_message.replace(bot_name, '')
    #     if 'm' in in_message or "whoareyou" in in_message:
    #        # print getMessages(webhook['data']['roomId'])

    #         msg = "Robot response!"

    #     elif 'batcave' in in_message:
    #         message = result.get('text').split('batcave')[1].strip(" ")
    #         if len(message) > 0:
    #             msg = "The Batcave echoes, '{0}'".format(message)
    #         else:
    #             msg = "The Batcave is silent..."
    #     elif 'batsignal' in in_message:
    #         print "NANA NANA NANA NANA"
    #         sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
    #     if msg != None:
    #         print msg
    #         sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
    return "true"


####CHANGE THESE VALUES#####
bot_email = "recapbot@gmail.com"
bot_name = "recapbot"
bearer = "OGM2MjljMzMtZTZiYS00YTc2LWJmOTUtZGFjNWY0YmZkZDUwZTlkNTg2N2QtNWUy"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"
run_itty(server='wsgiref', host='127.0.0.1', port=8080)
