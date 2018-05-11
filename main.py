
import tweepy, re, operator
from paralleldots import set_api_key, sentiment

# Authentication Consumer Key
CONSUMER_KEY = "xiW6mMJ9gk8kbpjtdON25yEfE"
CONSUMER_SECRET = "zz9jVz1GXAiViowmqqMMUpZsHCEkvthmbhxo1iOQ2FqYSUXppT"

# Authentication Access Tokens
ACCESS_TOKEN = "282487118-EhbdxPMP4aimPP2M9uRxXInbRfdEYzshVq9qE2jI"
ACCESS_TOKEN_SECRET = "qHcJRImZmO7FaVvaT3hB6CNflNa3nHLhcwUXXFP8DYtCB"


oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(oauth)

# defining tha main menu

def get_tweet():
    hash_tag = input("Enter the word without the hashtag")
    hash_tag = "#" + hash_tag
    print(hash_tag)
    tweets = api.search(hash_tag)
    return tweets


def test_sentiments():
    list_sents = []
    tweets = get_tweet()
    set_api_key("5Ilq8t88HXC0EYjVzpCDqqnQSlPJm5mJ9faJTnigwG4")
    for tweet in tweets:
        list_sents.append(sentiment(tweet.text))
    return list_sents


def tweet_match():
    trump = 0
    tweets = api.user_timeline(screen_name="@realdonaldtrump", count=200, tweet_mode="extended")
    for tweet in tweets:
        tweet_text = re.sub(r"http\S+", "", tweet.full_text)   # Removing the URL texts 
        if "India" in tweet_text or "INDIA" in tweet_text or "Bharat" in tweet_text or "Hindustan" in tweet_text or "india" in tweet_text:
            trump += 1

    modi = 0
    listx = []
    tweets = api.user_timeline(screen_name="@narendramodi", count=200, tweet_mode="extended")
    for tweet in tweets:
        listx.append(tweet.full_text)
    for x in listx:
        if "US" in x or "USA" in x or "America" in x or "United States Of America" in x or "america" in x:
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
    print("The Top Ten Words Are: ")
    for i in range(-1, -11, -1):
        print(sorted_dict[i][0], " - ", sorted_dict[i][1])





def menu():
    show_menu = True
    menu_choices = "\nEnter The Number Of the Corrosponding option:   \n1.Tweet Retrieval\n2.Count Followers\n3.Determine the Sentiments  \n4.Determine Location, Language, And Time Zone \n5.Comparison Of Tweets\n6.Top Words Usage\n7.Tweet A Message\n8.To Exit"
    while show_menu:
        choice = input(menu_choices)  # getting the user choice

        # For tweets Retrieval
        if choice == "1":
            tweets = get_tweet()   # getting the tweets from the other function
            print("Following tweets have been made by the people \n")
            for tweet in tweets:
                print(tweet.text)

        # Count Followers
        elif choice == "2":
            tweets = get_tweet()
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
            print("Sentiment Result:\nWait for a minute(max 2 min xD)")
            print("Positive:%d \t Negative:%d \t Neutral:%d" % (p, n, nu))

        # Determine the location
        elif choice == "4":
            pass
            # location

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






