from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
import json
import sys
import requests
import secrets # file that contains OAuth credentials
import nltk 
## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Wednesday, 9:00AM
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secrets.client_key
consumer_secret = secrets.client_secret
access_token = secrets.access_token
access_secret = secrets.access_token_secret
protected_url = 'https://api.twitter.com/1.1/account/settings.json'
oauth = OAuth1Session(consumer_key, consumer_secret, access_token, access_secret)

#Write your code below:
#Code for Part 3:Caching


CACHE_FNAME = 'twitter_cache.json'

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()
except:
	CACHE_DICTION = {}



def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)



def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = oauth.get(baseurl, params=params) #could be results.get
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]







#Code for Part 1:Get Tweets



def get_data(username,num_tweets):
	protected_url = 'https://api.twitter.com/1.1/search/tweets.json'
	params = {}
	params['q'] = str(username)
	params["count"] = str(num_tweets)
	return make_request_using_cache(protected_url,params) 




#STEP 2 OF PART 1
#results = json.loads(r.text)
#fp = open('tweets.json','w')
#json.dump(results,fp,sort_keys=True,indent=4)





#Code for Part 2:Analyze Tweets
results = get_data(username,num_tweets)

data = results['statuses']
strng = ""
for result in data:
	if 'text' in result:
		strng += result['text']

tokens = nltk.word_tokenize(strng)
freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and "www." not in token and "https" not in token)

for word, frequency in freqDist.most_common(5):
	print(word + " " + str(frequency))


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()