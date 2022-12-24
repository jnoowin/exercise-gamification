import twitter

def get_quest_tweet():
    CONSUMER_KEY = "lw6ldGwMQ3BZQ6WrLySNNTWpW"
    CONSUMER_SECRET = "l40cPW4aRYTQ3HUXFcZUJ0y3XSbyTE7otttRcuyqjrR594eIuX"
    ACCESS_TOKEN_KEY = "3232152077-st4L2IZm239Zj9Wuf5t3N1BWzMXiYKQB8lobRNX"
    ACCESS_TOKEN_SECRET = "7YZO0WTq0CK833yUojIhlO0LoOdgu2mTwU6ao12mdx7dI"

    api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET,
                      ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    timeline = api.GetUserTimeline(screen_name="maxlennon7", count=1)

    return timeline[0]
