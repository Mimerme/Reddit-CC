import praw, time
from praw.models import Comment
from youtube import get_captions_no_quota, get_automatic_captions
from urlparse import urlparse

print "Instantiating PRAW instance..."

#Credentials
#Create a new file called creds.txt in the same directory as this script
#Client ID First Line
#Client Secret Second Line
#Username 3rd Line
#Password 99th Line. jk 4th line
with open('creds.txt', 'r') as myfile:
    data=myfile.read().split("\n")

reddit = praw.Reddit(client_id=data[0],
                     client_secret=data[1],
                     username=data[2],
                     password=data[3],
                     user_agent='reddit-cc')

def is_youtube_video(comment_parent):
    #Must be a root comment
    if(comment_parent is Comment):
        return False
    url = comment_parent.url
    if(("youtube.com" in url) or ("youtu.be" in url)):
        return True
    else:
        return False
    
def get_captions(video_id, redditor, message_subject):
    captions = get_captions_no_quota(video_id)
    try:
        if(captions):
            return captions, True
        else:
            print "No manual captions. Using fallback"
            captions = get_automatic_captions(video_id)
            return captions, False
    except AttributeError:
        send_private_message(redditor, message_subject, "***Unable to find captions for the video***")

def send_private_message(redditor_name, message_subject, message_body):
    redditor_name.message(message_subject, message_body)

def send_batched_private_messages(captions, redditor, message_subject, start_message="", end_message=""):
    message_batch = []
    char_array = list(start_message + captions + end_message)
    #10,000 is the max length of a PM
    while len(char_array) > 10000:
        message_batch.append("".join(char_array[0:10000]))
        del(char_array[0:10000])
    message_batch.append("".join(char_array[0:]))

    for message in reversed(message_batch):
        send_private_message(redditor, message_subject, message)

#while True:
inbox = reddit.inbox
unread_message = []
print "Listening for new messages..."
for message in inbox.stream():
    message.mark_read()
    parent = message.submission
    if(isinstance(message, Comment) and (is_youtube_video(parent))):
        video_id = urlparse(parent.url)[4].replace("v=", "")
        captions, manual_captions = get_captions(video_id, parent.author, parent.title)
        if not manual_captions:
            send_batched_private_messages(captions, message.author, parent.title, "***AUTOMATIC CAPTIONS***")
        else:
            send_batched_private_messages(captions, message.author, parent.title, "***EN-US CAPTIONS***")
