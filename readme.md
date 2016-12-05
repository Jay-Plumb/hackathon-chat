### RecapBot

## Problem
Have you ever been in a group chat and want to be able to filter through the relevant information? Our recapbot uses a machine learning algorithm (bayes filter) to classify relevant from non relevant sentences.

## Tech Stack
* Spark Streaming
* Python for the backend
*Naive bayes filter

## Setup
A bot was created in spark and an ngrok tunnel was used to the webhook. A learning algorithm classifies the sentences and the size of the text it altered (the larger the font, the more relevant the information).

1. In terminal, call `ngrok http <portNumber>`
2. Generate webhook using [Spark for Developers website](https://developer.ciscospark.com/endpoint-webhooks-post.html)
  * In 'Request Headers', change Authorization to Bearer Token of the bot
  * Enter applicable 'Request Parameters' and Run
    [For the 'targetURL' field, enter the `Forwarding` URL generated by ngrok]
3. In another terminal, run *recapbot.py*
  * `python recapbot.py`

