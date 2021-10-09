# Fall 2021 Plextech Group 1
# WeatherFeed Project
##  Intro
After spending a bit of time on JavaScript, it's about time you apply what you have learned. In this project, you will not only be using JavaScript, but also dealing with API calls to get data that you wil display on the front end. In this project, you will be taking a random set of tweets about the weather and then displaying it as a feed. On top of this, you will also be updating the feed everytime there is a new tweet that is sent. You must also make sure that when updating the feed, there are no duplicate tweets in the feed. 
## Overview
### TwitterFeed API
You will be interacting with a server we’ve provided that will give you weather-related Tweets. The server is active at the following address:  [http://twitterfeedserverrails-env.eba-xmqy8ybh.us-east-1.elasticbeanstalk.com](http://twitterfeedserverrails-env.eba-xmqy8ybh.us-east-1.elasticbeanstalk.com/ "Twitter Feed Server address")
​
Make a GET request to the  [`/feed/random?q=weather`](http://twitterfeedserverrails-env.eba-xmqy8ybh.us-east-1.elasticbeanstalk.com/feed/random?q=weather "make request to random endpoint")  endpoint of the server ([example response](https://github.com/pengzhengyi/TwitterFeedServer/blob/master/example_responses/random.json)) to obtain a new block of 10 random Tweets.
​
The Chrome extension  [JSON Formatter](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en "JSON Formatter")  may be optionally used to more easily view the response, which will be returned as a JSON array.
​
Take note that some of these Tweets may be duplicates of Tweets that you’ve already seen, and it is your responsibility to filter those out. Every Tweet has a unique id field (`id`) that you can use for this purpose. Note that for the purposes of this assignment  retweets  count as their own tweets since they have a different id! Also note, for this assignment, we care about the tweet content (text) - it is possible to get a tweet object with different usernames/profiles but the same text content due to the mechanisms of our Twitter proxy server. If two tweets do have the same text content (are duplicates), those tweets are guaranteed to have the same id.
​
### Response
[The Search API's example response](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html)  describes what a success response from the server looks like.
​
The available properties for each tweet (represented by an object in  `statuses`  array) are  [those returned by the Twitter API for Tweets](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object).
​
In each tweet you’ll want to display at least the the  **author’s name**  and  **profile image**  ,  **the date in a readable format**  , and  **the text content for the tweet**  .
​
Note that some tweets you receive will be truncated by an ellipsis (...). This is okay as it is done by the API.
​
For displaying the date in a readable format, you may use the  [Moment.js library](https://momentjs.com/)  if you wish (the script is already imported for you in the stencil file).
### Guide
Since the idea of the TwitterFeed is that it’s a live stream of Tweets, having the entire page refresh every second with new content would be a bit annoying. Thus, the solution is to obtain the data in the background and update the page without refreshing it through JavaScript. There are multiple ways to do this, but we recommend using  [Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)  .
​
The standard template for a fetch request looks something like this:
```js
// specify a url, in this case our web server
const url = "http://twitterfeedserverrails-env.eba-xmqy8ybh.us-east-1.elasticbeanstalk.com/feed/random?q=weather"
​
fetch(url)
  .then(res => res.json())
  .then(data => {
  
    // do something with data
  })
  .catch(err => {
    // error catching
    console.log(err)
  })
```
Combine the above template with something like `setInterval(...)` (see [the Mozilla Developer Network’s documentation](https://developer.mozilla.org/en-US/docs/DOM/window.setInterval "mdn doc on setInterval") ) to periodically load new Tweets.
### Removing Duplicates
For duplicate checking, you should use `data.statuses[index].id` (id of the tweet) rather than `data.statuses[index].user.id` (id of the user who made the tweet). It may be a good idea to keep a list or [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) of ids that you have seen so far, as well as a master list that stores all the tweets that you might filter and sort on with the duplicates already removed.
### Sorting
Make sure to sort in chronological order

