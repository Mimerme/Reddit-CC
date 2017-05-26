import praw, time

print "Instantiating PRAW instance..."

#Credentials
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
                     
while True:
    for mention in reddit.inbox.mentions():
        print("Called @ " + str(mention))
        print("Marking " + str(mention) + " as read")
    time.sleep(10)
    
    