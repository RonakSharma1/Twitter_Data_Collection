# Aim
Within a user specified timeframe, this programme extracts the Twitter data (Tweets) that matches the user specified query parameters i.e. a list of hashtags and phrases

# Data Constraints
The programme filters out any retweets, replies, non-image tweets and also sanitises tweets by removing the non-ASCII characters. This was done on the request of the user.

# Result
1. 'Twitter_API_Result.csv': Stores the following information related to the data constrained tweets; Twitter Handle, Time Stamp, Tweet(Description), Names of Images associated to each Tweet,URL of images, URL of Tweets
2. Images are downloaded and stored locally using their URL extracted from Tweets  
3. 'Error_Log.txt': Logs any errors generated during the API call

# Structure of Folder
1. 'TwitterAPI_Socialmedia_Extract.py': Main Python file to run
2. 'credentials.txt': Contains the credentials of a Twitter Developer Account
3. 'hashtags.txt': Contains the list of hashtags (or any other query parameter) separated by ','. To understand the format of this file, check the Procedure Section


# Installation
1. Installing 'Tweepy' library in Anaconda on Mac OS
```
conda install -c conda-forge tweepy
```

# Procedure
1. Clone the 'credentials.txt' and replace the keys and tokens with the your credentials obtained via Twitter Developer Account

2. Clone the 'hashtags.txt' and enter the query parameters separated by ','.All the queries in the first row are OR'd. This expression is then AND'd with the OR'd query expressions of second row. Example:

2a. Row1: Science,Data 

2b. Row2: Research,Academic

2c. Final Query= (Science OR Data) AND (Research OR Academic)

3. Run 'TwitterAPI_Socialmedia_Extract.py'

# User Inputs
The following inputs need to be provided to run the algorithm
1. Start date of search (Cannot be more than 7 days from the current date due to Twitter Policy)
2. End data of search
3. Number of pages to be returned. Each page contains multiple tweets
4. Number of tweets to be returned per page

# Documentation
1. [Twitter Query Python Tutorial](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/social-media-text-mining-python/)
2. [Tweepy Documentation](https://github.com/tweepy/tweepy)
3. [Tweepy GitHub Repository](https://github.com/tweepy/tweepy)
