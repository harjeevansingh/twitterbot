### ACCESS TOKENS , CONSUMER KEY AND API_KEY(SENTIMENTS) HAVE BEEN REMOVED ####


import tweepy, re, operator
from paralleldots import set_api_key, sentiment

# Authentication Consumer Key
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

# Authentication Access Tokens
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""


oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(oauth)


def get_tweet():
    hash_tag = input("\nEnter the word without the hashtag")
    hash_tag = "#" + hash_tag
    tweets = api.search(hash_tag)
    return tweets


def test_sentiments():
    list_sents = []
    tweets = get_tweet()
    set_api_key("")
    for tweet in tweets:
        list_sents.append(sentiment(tweet.text))
    return list_sents


def location():
    lang = {}
    loc = {}
    time = {}
    tweets = get_tweet()
    for tweet in tweets:
        if tweet.user.lang in lang.keys():
            lang[tweet.user.lang] += 1
        else:
            lang[tweet.user.lang] = 1

        if tweet.user.location in loc.keys():
            loc[tweet.user.location] += 1
        elif tweet.user.location != '':
            loc[tweet.user.location] = 1

        if tweet.created_at in time.keys():
            time[str(tweet.created_at)] += 1
        else:
            time[str(tweet.user.created_at)] = 1

    print("\nNumber of times the languages used:")
    for (x, y) in lang.items():
        print("Language:%s \t Count:%d " % (x, y))

    print("\nNumber of posts from different Timezones:")
    for (x, y)in time.items():
        print("%s : %d" % (x, y))

    print("\nLocations from where posts were updated:")
    for (x, y) in loc.items():
        print("%s : %d" % (x, y))


def tweet_match():
    trump = 0
    tweets = api.user_timeline(screen_name="@realdonaldtrump", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts
        if "India" in tweet_text or "INDIA" in tweet_text or "Bharat" in tweet_text or "Hindustan" in tweet_text or "india" in tweet_text:
            trump += 1

    modi = 0
    tweets = api.user_timeline(screen_name="@narendramodi", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts
        if "US" in tweet_text or "USA" in tweet_text or "America" in tweet_text or "United States Of America" in tweet_text or "america" in tweet_text:
            modi += 1

    # showing the comparison
    print("MOdi-"+ str(modi))
    print("Trump-"+ str(trump))


def top_usage():
    import nltk
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    dictt = {}
    tweet_words = []
    tweet = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for x in tweet:
        y = x.full_text.split(" ")
        for z in y:
            tweet_words.append(z)
    for word in tweet_words:
        if word not in stop_words and "http" not in word:
            if word in dictt.keys():
                dictt[word] += 1
            else:
                dictt[word] = 1

    sorted_dict = sorted(dictt.items(), key=operator.itemgetter(1))
    print("\nThe Top Ten Words Are: ")
    for i in range(-1, -11, -1):
        print(sorted_dict[i][0], " - ", sorted_dict[i][1])


# defining tha main menu


def menu():
    show_menu = True
    menu_choices = "\nEnter The Number Of the Corrosponding option:   \n1.Tweet Retrieval\n2.Count Followers\n3.Determine the Sentiments  \n4.Determine Location, Language, And Time Zone \n5.Comparison Of Tweets\n6.Top Words Usage\n7.Tweet A Message\n8.To Exit"
    while show_menu:
        choice = input(menu_choices)  # getting the user choice

        # For tweets Retrieval
        if choice == "1":
            tweets = get_tweet()   # getting the tweets from the other function
            print("\nFollowing tweets have been made by the people: \n")
            for tweet in tweets:
                print(tweet.text)

        # Count Followers
        elif choice == "2":
            tweets = get_tweet()
            print("\nThe users along with the followers:")
            for tweet in tweets:
                print("User : %s \t Followers:%s " % (tweet.user.name, tweet.user.followers_count))
            print("\n")

        # Determine The Sentiments
        elif choice == "3":
            list_sents = test_sentiments()
            p = 0
            n = 0
            nu = 0
            for x in list_sents:
                if x["sentiment"] == "neutral":
                    nu += 1
                elif x["sentiment"] == "negative":
                    n += 1
                elif x["sentiment"] == "positive":
                    p += 1
            print("Sentiment Result:\n")
            print("Positive:%d \t Negative:%d \t Neutral:%d" % (p, n, nu))

        # Determine the location
        elif choice == "4":
            location()

        # Comparison of tweets
        elif choice == "5":
            tweet_match()

        # Top Usage
        elif choice == "6":
            top_usage()

        # Tweet A Message
        elif choice == "7":
            status = input("Enter The Status update:")
            api.update_status(status)

        # Exit
        elif choice == "8":
            show_menu = False


menu()
