####################
## Import modules ##
####################

import random
import datetime
from datetime import timedelta
import time
import sys
import facebook
from pymongo import MongoClient
import fbchat


##############################
## Init Facebook Connection ##
##############################


def fb_connect():
    access_token = TOKEN 
    graph = facebook.GraphAPI(access_token)
    return (graph)


##############################


################################
## Get group ID by group name ##
################################


def get_group_id(graph, group_name):
    user_groups = graph.get_object('/me/groups')
    for i in range(0, len(user_groups['data'])):
        if (user_groups['data'][i]['name'] == group_name):
            return (user_groups['data'][i]['id'])
    return "Error"



##############################


#######################
## Get feed of group ##
#######################


def get_new_post(graph, time, group_id):
    request = group_id + '/feed?since=' + str(time) + \
                "&fields=id,comments,attachments&limit=100"
    feed = graph.get_object(request)
    return (feed)


##############################


##################
## Get posts id ##
##################


def get_post_ids(feed):
    ids = []
    for i in range(0, len(feed['data'])):
        ids.append(feed['data'][i]['id'])
    return (ids)


##############################


############################
## Verify single comments ##
############################


def verify_message(comment_message, comment_tags):
    names = []
    x = 0
    try:
        if len(comment_tags) > 0 and comment_tags[0]['type'] != "user":
            return 0
    except KeyError:
        l = 2
    for i in range(0, len(comment_tags)):
        try:
            names.append(comment_tags[i]['name'].split())
        except KeyError:
            print("User banned")
    comment_message = comment_message.split()
    for i in range(0, len(comment_message)):
        p = 0
        for j in range(0, len(names)):
            if (comment_message[i] not in names[j]):
                p = p + 1
        if p == len(names):
            x = x + 1
    if (x == 0):
        return (1)
    return (0)


###########################


#########################
## Verify all comments ##
#########################


def get_number_of_warnings(user_id, warnings):
    number = warnings.find({"id" : user_id})
    i = 0
    for var in number:
        i = i + 1
    return i


def not_replied(graph, comment):
    request = comment + '/comments'
    all_replies = graph.get_object(request)
    for i in range(0, len(all_replies['data'])):
        if (all_replies['data'][i]['from']['id'] == BOT_ID): ## Modify with your bot ID
            return 0
    return 1


def check_wrong_comment(post_ids, graph, db, friend, chat):
    for i in range(0, len(post_ids)):  
        post_id = post_ids[i]
        request1 = post_id + '/comments?fields=message_tags,message,from&limit=200'
        all_tags = graph.get_object(request1)
        for j in range(0, len(all_tags['data'])):
            comment = all_tags['data'][j]
            if ("message_tags" in comment and verify_message(comment['message'], comment['message_tags']) == 1):
                new_message = [FIRST_MESSAGE, SECOND_MESSAGE]
                if (not_replied(graph, comment['id']) == 1):
                    warning = {"name": comment['from']['name'],
                               "id": comment['from']['id'],
                               "reason": comment['message']}
                    warnings = db.warnings ## Write in the database with the warnings you set up
                    nb = get_number_of_warnings(comment['from']['id'], warnings)
                    if nb == 2:
                        x = 3
                        for l in range(0, len(friend)):
                            try:
                                chat.send(friend[l].uid, CHAT_MESSAGE) 
                            except UnicodeEncodeError:
                                print("Unicode error")
                    if nb <= 2 and nb >= 0:
                        warning_id = warnings.insert(warning)
                        print("\ncomment id = : " + comment['id'])
                        try:
                            graph.put_comment(object_id=comment['id'], message=new_message[nb])
                        except:
                            print("Facebook error")

##############################


global BOT_ID         = "",
       TOKEN          = "",
       EMAIL          = "",
       PASSWORD       = "",
       FIRST_MESSAGE  = "",
       SECOND_MESSAGE = "",
       CHAT_MESSAGE   = "",
       REFRESH_RATE   =         


#########################
## Init facebook group ##
#########################


graph = fb_connect()

group_name = GROUP_NAME
group_id = GROUP_ID ## Use this if you know it, because you will do less requests
group_id = get_group_id(graph, group_name) ## Use that only if you dont know the id of your group
if (group_id == "Error"):
    print("Error in group name")
    exit(-1)


##############################


############################
## Init database and chat ##
############################


client = MongoClient()
db = client.logs

name = ["YOUR FIRST FRIEND", "YOUR SECOND FRIEND"] # And so on
chat = fbchat.Client(EMAIL, PASSWORD)
friends = []
for t in range(0, len(name)):
    friends.append(chat.getUsers(name[t])[0])


##############################


###############
## Main Loop ##
###############


print("")
while (1):
    week = timedelta(days=7)
    timestamp1 = datetime.datetime.now().replace(microsecond=0)
    timestamp1_m = int(time.time()) 
    while (1):
        try:
            timestamp2 = datetime.datetime.now().replace(microsecond=0)
        except KeyboardInterrupt:
            exit(0)
        feed = get_new_post(graph, timestamp1_m, group_id)
        i = 0
        while len(feed['data']) == 100 or i == 0:
            print "len = %d" % len(feed['data'])
            i = i + 1
            post_ids = get_post_ids(feed)
            check_wrong_comment(post_ids, graph, db, friends, chat)
            if len(feed) == 2:
                page = feed['paging']['next'].split("v2.2/")
                try:
                    feed = graph.get_object(page[1])
                    print("Getting next page !")
                except:
                    print("Timeout 2")
        print "len = %d" % len(feed['data'])
        if (timestamp2 - week) == timestamp1: ## Refresh the feed of the group every week
            break
        print("Starting to sleep")
        for i in xrange(4,0,-1):
            time.sleep(REFRESH_RATE)
            sys.stdout.write(str(i)+' ')
            sys.stdout.flush()
        print("\nRotating back\n")
        

##############################
