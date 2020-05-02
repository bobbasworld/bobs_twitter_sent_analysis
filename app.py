
from textblob import TextBlob
import sys, tweepy, os
import matplotlib.pyplot as plt

from dotenv import load_dotenv
load_dotenv()


apiKey = os.environ.get("apiKey")
apiSecret = os.environ.get("apiSecret")
accessToken = os.environ.get("accessToken")
accessTokenSecret = os.environ.get("accessTokenSecret")

def percentage(part, whole):
    return 100 * float(part)/float(whole)

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

searchTerm = input("Enter a keyword to anaylyse sentiment: ")
searchTermCount = int(input("Enter the number of tweets to analyze: "))

tweets = tweepy.Cursor(api.search, q=searchTerm).items(searchTermCount)

# tweets = api.search(q=searchTerm, count=searchTermCount)

positive = 0
negative = 0
neutral = 0
polarity = 0

for tweet in tweets:
    # print(tweet.text)
    analysis = TextBlob(tweet.text)
    polarity += analysis.sentiment.polarity

    if (analysis.sentiment.polarity == 0):
        neutral += 1
    
    elif (analysis.sentiment.polarity < 0.00):
        negative += 1
    
    elif (analysis.sentiment.polarity > 0.00):
        positive += 1

postive = percentage(positive, searchTermCount)
negative = percentage(negative, searchTermCount)
neutral = percentage(neutral, searchTermCount)
polarity = percentage(polarity, searchTermCount)

# format to 2dp
positive = format(positive, ".2f")
neutral = format(neutral, ".2f")
negative = format(negative, ".2f")

# print results
if (polarity == 0):
    print("Neutral")

elif (polarity < 0):
    print("Negative")

elif (polarity > 0):
    print("Positive")

# Print Pie Chart
labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('Twitter Users Sentiment on ' + searchTerm + ' by analyzing ' + str(searchTermCount) + ' Tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()

