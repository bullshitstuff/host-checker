import requests
import os
import json
import sys
import time

# Function to send a message to the Telegram bot
def send_message(bot_message):
    # Get the bot token and chat ID from the environment variables
    bot_token = os.environ.get("TOKEN")
    bot_chat_id = os.environ.get("CHATID")
    
    # Create the message URL with the bot token, chat ID and message
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&disable_web_page_preview=true&text=' + bot_message
    
    # Send the message using the URL and get the response
    response = requests.get(send_text)
    
    return response.json()

# Get a list of domains from the environment variable and split them by comma
domain_list = []
domain_list = str(os.environ.get("DOMAIN")).split(",")

# Loop through each domain in the list
for domain in domain_list:
    # Send a request to check the HTTP status of the domain
    check_request = requests.post('https://check-host.net/check-http?host='+domain+'&node=ir4.node.check-host.net&node=ir3.node.check-host.net&node=ir1.node.check-host.net', headers={'Accept': 'application/json'})
    
    # Wait for 10 seconds before sending the next request
    time.sleep(10)
    
    # Send a request to get the result of the previous request
    check_result = requests.post('https://check-host.net/check-result/'+check_request.json()["request_id"], headers={'Accept': 'application/json'})
    
    # If the domain is down, send a message to the Telegram
    if "Connection timed out" in check_result.text:
        send_message(domain + " is down. ⚠️⚠️⚠️⚠️⚠️⚠️")