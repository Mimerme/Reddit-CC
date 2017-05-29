import praw, time
from praw.models import Comment
from youtube import get_captions_no_quota, get_automatic_captions

print "Instantiating PRAW instance..."

#Credentials
#Create a new file called creds.txt in the same directory as this script
#Client ID First Line
#Client Secret Second Line
#Username 3rd Line
#Password 99th Line. jk 4th line
with open('creds.txt', 'r') as myfile:
    data=myfile.read().split("\n")

def is_youtube_video(comment_parent):
    #Must be a root comment
    if(comment_parent is Comment):
        return False
    url = comment_parent.url
    if(("youtube.com" in url) or ("youtu.be" in url)):
        return True
    else:
        return False
    
def get_captions(video_id):
    captions = get_captions_no_quota(video_id)
    if(captions):
        return captions 
    else:
        print "No manual captions. Using fallback"
        captions = get_automatic_captions(video_id)
        return captions

reddit = praw.Reddit(client_id=data[0],
                     client_secret=data[1],
                     username=data[2],
                     password=data[3],
                     user_agent='reddit-cc')

#while True:
inbox = reddit.inbox
unread_message = []
for message in inbox.stream():
    print message
    message.mark_read()
    parent = message.parent()
    if((message is Comment) and (is_youtube_video(message.parent()))):
        print parent.url
        captions = get_captions(parent.url)
        message.reply

