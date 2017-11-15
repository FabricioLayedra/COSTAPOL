
# coding: utf-8

# In[4]:


import pandas as pd
import simplejson as json
import unicodedata
import matplotlib.pyplot as plt
from os import listdir


# In[66]:


num_tweets = 0
invalid_tweets = 0
for fil in fils:
    name = path + fil
    g = json.loads(open(name).read())
    ###condicion de que sea retweet
    tweets = g["tweets"]
    num_tweets += g["num_tweets"]
    for tweet in tweets:
        if isValid(tweet) :
            invalid_tweets +=1
print num_tweets, invalid_tweets


# In[71]:


frequency_file = open("../Outputs/frequencies.csv","w")
frequency_file.write("user,num_tweets,num_vtweets,num_rts,num_favs\n")
mentioned = dict()
hashtags = dict()

for fil in fils:
    g = json.loads(open(fil).read())

    num_tweets = g["num_tweets"]
    tweets = g["tweets"]
    user = fil.split("/")[3].split(".")[0]
    valids = 0
    nrts = 0
    nfavs = 0
    mentioned[user]= set()
    hashtags[user]= dict()
    for tweet in tweets:
        valid = True
        for url in tweet["entities"]["urls"]:
            print url["display_url"]
            if url["display_url"] == "fllwrs.com":
                valid = False  
                print "entro"
        if valid :
            nrts += tweet["retweet_count"]
            nfavs += tweet["favorite_count"]
            valids +=1
            for mention in tweet["entities"]["user_mentions"]:
                s = mention["screen_name"]
                d = ''.join((c for c in unicodedata.normalize('NFD', unicode(s)) if unicodedata.category(c) != 'Mn'))
                mentioned[user].add(d)
            for hashtag in tweet["entities"]["hashtags"]:
                s = hashtag["text"]
                d = ''.join((c for c in unicodedata.normalize('NFD', unicode(s)) if unicodedata.category(c) != 'Mn'))
                if d in hashtags[user]:
                    hashtags[user][d] +=1
                else:
                    hashtags[user][d] = 1
    frequency_file.write("%s,%d,%d,%d,%d\n"%(user,num_tweets,valids,nrts,nfavs))
    for user in mentioned:
        mentions_file = open("../Outputs/mentions/%s_mentions.csv"%user,"w")
        mentions_file.write("user,mentioned_user")
        
        for mention in mentioned[user]:
            mentions_file.write("%s,%s\n"%(user,mention))
        mentions_file.close()
    for user in hashtags:
        hashtags_file = open("../Outputs/hashtags/%s_mentions.csv"%user,"w")
        hashtags_file.write("hashtag,frequency\n")
        
        for hashtag,freq in hashtags[user].items():
            hashtag = str(hashtag)
            freq= str(freq)
            linet = hashtag + "," + freq + "\n"
            hashtags_file.write(linet)
        hashtags_file.close()             
frequency_file.close()


# In[121]:


fils = listdir("../Data/timeline/manta/")
path = "../Data/timeline/manta/"

def isRetweet(tweet):
	texto = tweet['text']
	if 'retweeted_status' in tweet or (len(texto) > 4 and texto[:4] == 'RT @'):
		return True
	return False

def isValid(tweet):
    for url in tweet["entities"]["urls"]:
        #print url["display_url"]
        if url["display_url"] == "fllwrs.com":
            return False 
    return True
    
            


# In[15]:


mentions_file = open("../Outputs/mentions.csv","w")
mentions_file.write("source,target,weight\n")

mentions = dict()
for fil in fils:
    name = path + fil
    g = json.loads(open(name).read())
    ###condicion de que sea retweet
    num_tweets = g["num_tweets"]
    tweets = g["tweets"]
    user = name.split("/")[4].split(".")[0]
    valids = 0
    for tweet in tweets:
        if isValid(tweet) and isRetweet(tweet):
            #print tweet
            for people in tweet["entities"]["user_mentions"]:
                if (user,people["screen_name"]) in mentions:
                    mentions[user,(people["screen_name"])] +=1
                else:
                    mentions[user,(people["screen_name"])] =1

for mention in mentions:
    source,target = mention
    mentions_file.write(source + ","+ target + ","+ str(mentions[mention])+"\n")
mentions_file.close()


# In[52]:


hashtags_file = open("../Outputs/hashtags.csv","w")
hashtags_file.write("user,hashtag,frequency\n")

hashtags = dict()
for fil in fils:
    name = path + fil
    g = json.loads(open(name).read())
    ###condicion de que sea retweet
    num_tweets = g["num_tweets"]
    tweets = g["tweets"]
    user = name.split("/")[4].split(".")[0]
    valids = 0
    hashtags[user]= dict()
    for tweet in tweets:
        if isValid(tweet):
            #print tweet
            for hashtag in tweet["entities"]["hashtags"]:
                s = hashtag["text"]
                #print s
                d = ''.join((c for c in unicodedata.normalize('NFD', unicode(s)) if unicodedata.category(c) != 'Mn'))
                if d in hashtags[user]:
                    hashtags[user][d] +=1
                else:
                    hashtags[user][d] = 1
                    #print hashtags[user]

for user in hashtags:
    for hashtag in hashtags[user]:
        freq = hashtags[user][hashtag]
        line = user+ ","+ hashtag + ","+ str(freq)+"\n"
        print line
        hashtags_file.write(line)
hashtags_file.close()


# In[81]:


df = pd.read_csv("../Outputs/frequencies.csv")
df.head()


# In[82]:


df["norm_rt_activity"]= df["num_rts"]/df["num_vtweets"]
df.head()

df["norm_fav_activity"]= df["num_favs"]/df["num_vtweets"]
ds = df[["user","norm_rt_activity","norm_fav_activity"]] 
ds.set_index(["user"],inplace=True)
ds.plot(kind='scatter',alpha=0.75, rot=90)
print ds.head()
plt.show()


# In[89]:


import seaborn as sns
par = sns.pairplot(ds)
plt.show()


# In[29]:


import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
 
print elimina_tildes(u"cóñrcholis")


# In[35]:


import seaborn as sns
df = pd.read_csv("../Outputs/mentions.csv")
ds = df[df["weight"]>5]
ds.to_csv("../Outputs/mentions_plus5.csv")


# In[39]:


f = open("../Outputs/mentions_plus5.csv")
nodes = set()
for line in f:
    id, source,target, freq = line.split(",")
    nodes.add(source)
    nodes.add(target)
f.close()
f = open("../Outputs/nodes_mentions_plus5.csv","w")
f.write("id,label\n")
for element in nodes:
    f.write("%s,%s\n"%(element,element))
f.close()


# In[118]:


import time
from datetime import datetime
import pytz
from email.utils import parsedate_tz, mktime_tz

def isRetweet(tweet):
	texto = tweet['text']
	if 'retweeted_status' in tweet or (len(texto) > 4 and texto[:4] == 'RT @'):
		return True
	return False

def getRetweetCount(tweet):
	return tweet['retweet_count']

def getFavoriteCount(tweet):
	return tweet['favorite_count']

def fillWeekHours(user_info):
    for day in user_info['days']:
        for month in range(1,13):
            user_info['days'][day][month] = {}
            for hour in range(24):
                user_info['days'][day][month][hour] = {}
                user_info['days'][day][month][hour]['retweet_count'] = 0
                user_info['days'][day][month][hour]['favorite_count'] = 0

def get_num_tweets(filen):
    d = json.loads(open(path+filen).read())
    result = d["num_tweets"]
    for t in d["tweets"]:
        if not isValid(t) or isRetweet(t):
            result = result -1
    return result
            
def getUsersWeeklyHourData(users_list):

	f = open('users_basic_data1.csv', 'w')
	f.write('username,retweet_count,favorite_count,num_tweets,month,day,hour\n')
	for username in users_list:
		user_info = { 'days': {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}}
		user_info['username'] = username
		fillWeekHours(user_info)
		user_data = json.loads(open(path+username).read())
		tweets = user_data['tweets']
        user_info["num_tweets"] = get_num_tweets(username)
        for tweet in tweets:
            timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
            dt = datetime.fromtimestamp(timestamp, pytz.timezone('US/Central'))
            weekday = dt.weekday()
            hour = dt.hour
            month = dt.month
            if not isRetweet(tweet):
                user_info['days'][weekday][month][hour]['retweet_count'] += getRetweetCount(tweet)
                user_info['days'][weekday][month][hour]['favorite_count'] += getFavoriteCount(tweet)
            writeUserWeeklyHourData(user_info, f)
        f.close()

def writeUserWeeklyHourData(user_info, f):
	username = user_info['username']
	for day in user_info['days']:
		for month in user_info['days'][day]:
			for hour in user_info['days'][day][month]:
				retweet_count = user_info['days'][day][month][hour]['retweet_count']
				favorite_count = user_info['days'][day][month][hour]['favorite_count']
				f.write(username + ',' + str(retweet_count) + ',' + str(favorite_count) + ','+ str(user_info["num_tweets"]))
				f.write(str(month) + ',' + str(day) + ',' + str(hour) + '\n')

getUsersWeeklyHourData(fils)


# In[125]:


de = pd.read_csv("users_basic_data.csv")
de["username"] = de["username"].apply(lambda x: x.split(".")[0])




# In[190]:


dist = de.groupby(["month"]).sum()[["retweet_count"]]
dist.plot()
plt.show()


# In[134]:


aceptacion = de.groupby(["username"]).sum()[["retweet_count","favorite_count"]]


# In[191]:


aceptacion.value_counts()


# In[182]:


q=de.groupby(["month","day"]).sum().loc[(10,)]


# In[183]:


del q["hour"]


# In[184]:


import pylab
q.plot(kind='line')

plt.savefig('oct.png')


# In[178]:


de

