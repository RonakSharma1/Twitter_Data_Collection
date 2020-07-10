#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:50:09 2020

@author: ronaksharma
"""

# Guide
# http://docs.tweepy.org/en/latest/
# https://github.com/tweepy/tweepy
# Tutorial: https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/social-media-text-mining-python/
# API methods: http://docs.tweepy.org/en/latest/api.html#api-reference

# Installtion of library for Anaconda
# conda install -c conda-forge tweepy
   
# Libraries
import tweepy
import re
#import pandas
#------------ Functions--------#
def separateUrl(tweet):
    urlRegex = re.compile(r'https?://\S+|www\.\S+')  # Regular expression to identify URLs in a tweet
    url = re.findall(urlRegex,tweet)
    tweetURL=url[-1] #The last URL in a tweet is the valid image URL
    tweetWithoutURL = urlRegex.sub(r'', tweet)
    return tweetURL,tweetWithoutURL

#-----------------------------#



#-------------Reading credentials to access Twitter API-------------------#
# Each line is stored as an element in the list. Each element is then split
# at '=' character and then the trailing '\n' is removed.
with open('credentials.txt','r') as listOfCredentials:
   credentials=listOfCredentials.readlines()
   consumer_key=(credentials[0].split('=')[1]).strip()
   consumer_secret=(credentials[1].split('=')[1]).strip()
   access_token=(credentials[2].split('=')[1]).strip()
   access_token_secret=(credentials[3].split('=')[1]).strip()

#--------Reading hashtags to access input contraints--------------------#
with open('hashtags.txt','r') as listOfHashtags:
   hashtags=listOfHashtags.readline()
   hashtags=hashtags.split(',')
   twitterQuery=' OR '.join(hashtags)

#---Search Paramters-----#
twitterFilter= " -filter:retweets" + " filter:twimg"# Filtering on tweets with images and removing any retweets
finalSearchQuery=twitterQuery+twitterFilter
startDate = "2020-07-05"
endDate="2020-07-11" # Exclusive of the date. +1 this argument to include the date
numberOfTweets=7
listOfTweets=[]
listOfUserName=[]
listOfDate=[]
listOfTime=[]
listOfTweetURL=[]
listOfMediaURL=[]
x=[]

#------- Authentication and Authorisation-----------#
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) # Using tweepy's API class
# Setting the 'rate_limit' arguments pauses the programe and notifies the user when limit reached than throwing an error

#-----Posting a Tweet-----#
#api.update_status("First tweet using #Python")

#-- Fetching Timeline data----#
#for tweet in tweepy.Cursor(api.user_timeline).items(3): # Pagination allows to specify the amount of pages to extract information from
##for tweet in publicTweets:
#    print(tweet.text)

#--- Fetching Hashtag Data-----#
listOfTweetsAttributes=tweepy.Cursor(api.search,
                                     q=finalSearchQuery, # Search Query
                                     lang='en', # Language
                                     since=startDate, until=endDate,
                                     result_type='recent', # Returns recent tweets
                                     tweet_mode='extended', # Prevent getting truncated response as the return limit is 140 characters
                                     exclude_replies=True,
                                     include_entities=True,
                                     monitor_rate_limit=True).items(numberOfTweets)
for tweet in listOfTweetsAttributes:
    #-------Processing raw date time data------------#
    dateTimeRawInformation=tweet.created_at # Time Stamps of tweets
    date=dateTimeRawInformation.strftime("%d %b %Y ") # Extracting date information
    time=dateTimeRawInformation.strftime("%H:%M:%S") # Extracting time information
    x.append(tweet.full_text)
    
    #------ Sanitising tweet caption----------#
    tweetURL,tweetWithoutURL=separateUrl(tweet.full_text)
    
    #----- Storing the meta data in a list ------------#
    for image in  tweet.entities['media']: # Looping through all media entities associated with that tweet
        listOfMediaURL.append(image['media_url']) # Accesing the 'url' attribute of that media
    listOfDate.append(date) # Timestamp of the tweet
    listOfTime.append(time)
    listOfUserName.append(tweet.user.screen_name) #User name
    listOfTweets.append(tweetWithoutURL) # Tweet Captions
    listOfTweetURL.append(tweetURL)
    