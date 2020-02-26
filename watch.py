URL = "https://www.kickstarter.com/projects/soontech/regium-automatic-chess-e-board-0/stats.json?v=1"
import requests
import time
import os
import slack

from dotenv import load_dotenv
load_dotenv()

slack_token = os.environ["SLACK_API_TOKEN"]
client = slack.WebClient(token=slack_token)
channel_id = os.environ["CHANNEL_ID"]
user_id = os.environ["USER_ID"]

def post_price_change(r):
    diff = r['pledged'] - previous['pledged']
    if diff > 0:
        emoji = ":rocket:"
    else:
        emoji = ":chart_with_downwards_trend:"
    client.chat_postMessage(
      channel=channel_id,
      text=f":mensa: update. Pledged: {r['pledged']}, Diff: {r['pledged'] - previous['pledged']}. {emoji}",
      as_user=user_id
    )


previous = {'pledged': 50000.0}
while True:
    print("Checking ...", end='')
    r = requests.get(URL).json().get('project', {})
    print("done.")
    if r.get('pledged'):
        r['pledged'] = float(r['pledged'])
    if r != previous:
        post_price_change(r)
        previous = r

    time.sleep(5)
