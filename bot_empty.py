import requests
import time
import tweepy
import api_cred

already_tweeted = False
info_dict = {
    "title": "none", 
    "tweet_id": 0}

# twitter authentication here, I don't think I have to put it in the while loop, checked once should be fine
auth_twitter = tweepy.OAuthHandler(api_cred.twitter_api_key, api_cred.twitter_api_secret)
auth_twitter.set_access_token(api_cred.twitter_access_token, api_cred.twitter_access_secret)
twitter_api = tweepy.API(auth_twitter)

# function to change the sleep time whether the stream is live or not. When live the wait is longer.
def refresh_rate():
    if stream_is_live:
        return 120
    else:
        return 60

# main function for live checking and tweeting
def twitter_bot():
    global already_tweeted
    global stream_is_live

    # twitch API stuff. This has to be here so it updates
    response = requests.get(api_cred.api_url, headers=api_cred.HEADERS)
    stream_is_live = response.json()["data"][0]["is_live"]
    stream_title = response.json()["data"][0]["title"]
    # stream_category = response.json()["data"][0]["game_id"]  # I don't know how to read it
    stream_url = "https://www.twitch.tv/<streamer_nickname>"

    tweets_content = {
        "tweet_stream": f".@<Twitter_handle> IS LIVE!\n\n{stream_title}\n\n{stream_url}",
        "tweet_change_title": f".@<Twitter_handle> IS STILL LIVE!\n\n{stream_title}\n\n{stream_url}",
        "test": ".@<Twitter_handle> it's just a test 3"}

    if stream_is_live and not already_tweeted:
        info_dict["title"] = stream_title
        # reference here https://github.com/tweepy/tweepy/issues/768 for try/except

        try:
            first_tweet = twitter_api.update_status(tweets_content["tweet_stream"])
            info_dict["tweet_id"] = first_tweet.id
            already_tweeted = True
        except tweepy.TweepError:
            try:
                not_duplicate_tweet = info_dict["tweet_stream"] + "\n."
                first_tweet = twitter_api.update_status(not_duplicate_tweet)
                info_dict["tweet_id"] = first_tweet.id
                already_tweeted = True
            except tweepy.TweepError:
                not_duplicate_tweet_2 = info_dict["tweet_stream"] + "\n..."
                first_tweet = twitter_api.update_status(not_duplicate_tweet_2)
                info_dict["tweet_id"] = first_tweet.id
                already_tweeted = True

        print("STATUS: LIVE POGGERS")
        print("TITLE: " + info_dict["title"])
    elif stream_title != info_dict.get("title") and already_tweeted is True and stream_is_live:
        info_dict["title"] = stream_title

        try:
            second_tweet = twitter_api.update_status(tweets_content["tweet_change_title"], info_dict["tweet_id"])
            info_dict["tweet_id"] = second_tweet.id
        except tweepy.TweepError:
            try:
                not_duplicate_answer = info_dict["tweet_change_title"] + "\n."
                second_tweet = twitter_api.update_status(not_duplicate_answer, info_dict["tweet_id"])
                info_dict["tweet_id"] = second_tweet.id
            except tweepy.TweepError:
                not_duplicate_answer_2 = info_dict["tweet_change_title"] + "\n..."
                second_tweet = twitter_api.update_status(not_duplicate_answer_2, info_dict["tweet_id"])
                info_dict["tweet_id"] = second_tweet.id

        print("STATUS: NEW TITLE PogU")
        print("TITLE: " + info_dict["title"])
    elif not stream_is_live:
        print("STATUS: Not live ResidentSleeper")
        if info_dict["title"] != "none":
            info_dict["title"] = "none"
        if already_tweeted:
            already_tweeted = False
    else:
        print("STATUS: LIVE -- NO CHANGE")
        print("TITLE: " + info_dict["title"])

    time.sleep(refresh_rate())
    # time.sleep(20)  # definetely don't make this 2 seconds, I think 60 seconds will be fine

while True:
    twitter_bot()