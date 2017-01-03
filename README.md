## Synopsis

A quick bot for Facebook

## Motivation

I felt like I needed to implement this bot to help the moderators in their daily work

## Installation

You need to install python 2.7 and install the mongoDB server which can be found here : 
`https://www.mongodb.com/download-center`

Follow these steps to get the bot to work :

- `pip install virtualenv`

- `virtualenv facebookenv`

- `source facebookenv/bin/activate`

- `pip install -e git+https://github.com/mobolic/facebook-sdk#egg=facebook-sdk`

- `pip install fbchat mongodb`

- `mongod --dbpath YOUR_DB_NAME`

You need a Facebook account that is admin on the group you want to moderate

You also need to figure out how to get a token with priviledges

## Functionalities

- Find comment that match the criteria, in this case where the only text is tagged people  

- Store their names in a MongoDB Database

- When their names appear x times in the Database, send yourself a message with a link to the comment

## Futur functionalities

- Photo recognition for repost (you will be able to send a photo to the bot, and it will tell you if it has already been posted)

## API Reference

Python Facebook SDK : https://github.com/mobolic/facebook-sdk