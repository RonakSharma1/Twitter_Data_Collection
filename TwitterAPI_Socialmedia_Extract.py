#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:50:09 2020

@author: ronaksharma
"""

# Guide
# http://docs.tweepy.org/en/latest/
# https://github.com/tweepy/tweepy
# API methods: http://docs.tweepy.org/en/latest/api.html#api-reference

# Installtion of library for Anaconda
# conda install -c conda-forge tweepy

# Libraries
import tweepy
#import pandas

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
startDate = "2020-07-03"
endDate="2020-07-08" # Exclusive of the date. +1 this argument to include the date
numberOfTweets=7
listOfTweets=[]
listOfUserName=[]
listOfDate=[]
listOfTime=[]

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
                                     q=finalSearchQuery,
                                     lang='en',
                                     since=startDate, until=endDate,
                                     result_type='recent',
                                     monitor_rate_limit=True).items(numberOfTweets)
for tweet in listOfTweetsAttributes:
    #-------Processing raw data------------#
    dateTimeRawInformation=tweet.created_at # Time Stamps of tweets
    date=dateTimeRawInformation.strftime("%d %b %Y ") # Extracting date information
    time=dateTimeRawInformation.strftime("%H:%M:%S") # Extracting time information
    
    #----- Storing the meta data in a list ------------#
    listOfDate.append(date) # Timestamp of the tweet
    listOfTime.append(time)
    listOfUserName.append(tweet.user.screen_name) #User name
    listOfTweets.append(tweet.text) # Tweet Captions
