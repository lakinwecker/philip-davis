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

def post_change(r):
    message = ":mensa: update."
    backers_count_diff = r['backers_count'] - previous['backers_count']
    if backers_count_diff != 0:
        message +=  " # of backers change: {backers_count_diff}"

    comments_count_diff = r['comments_count'] - previous['comments_count']
    if comments_count_diff != 0:
        message +=  " # of comments change: {comments_count_diff}"

    pledged_diff = r['pledged'] - previous['pledged']
    if pledged_diff != 0:
        if pledged_diff > 0:
            emoji = ":rocket:"
        else:
            emoji = ":chart_with_downwards_trend:"
        message += f" Pledge change: from ${previous['pledged']:.2f} to ${r['pledged']:.2f} = {pledged_diff:.2f}. {emoji}"
    print(message)
    client.chat_postMessage(channel=channel_id, text=message, as_user=user_id)


previous = {}
while True:
    try:
        print("Checking ...", end='')
        r = requests.get(URL).json().get('project', {})
        print("done.")
        if r.get('pledged'):
            r['pledged'] = float(r['pledged'])
        if not previous:
            previous = r
        elif r != previous:
            post_change(r)
            previous = r
    except:
        import traceback
        print(traceback.format_exc())

    time.sleep(60)
