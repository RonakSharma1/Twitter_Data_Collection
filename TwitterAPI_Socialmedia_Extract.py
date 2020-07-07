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

#-------------Reading credentials to access Twitter API-------------------#
# Each line is stored as an element in the list. Each element is then split
# at '=' character and then the trailing '\n' is removed.
with open('credentials.txt','r') as listOfCredentials:
   credentials=listOfCredentials.readlines()
   consumer_key=(credentials[0].split('=')[1]).rstrip()
   consumer_secret=(credentials[1].split('=')[1]).rstrip()
   access_token=(credentials[2].split('=')[1]).rstrip()
   access_token_secret=(credentials[3].split('=')[1]).rstrip()












# General Knowledge
# 1. Twitter does not expire tokens. So can save tokens to re-use later