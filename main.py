#Made by /u/sagiksp
#Modified by HeyItsShuga and Cth1003 (added more triggers + comments)

username="BOT_USERNAME" #BOTS NAME
password="BOT_PASSWORD" #BOTS PASSWORD
creator_name="YOUR_NAME" #YOUR NAME (WITHOUT THE /U/)
bot_subreddit="BOT_USERNAME_SUBREDDIT" #BOTS SUBREDDIT

import praw, time, re #Imports needed modules for bot to run.

#Variables

user_agent="Cant Hear You by /u/"+creator_name #The name the bot will use to communicate with reddit.
users = [] #People that have been yelled at. Format: [[Username,UTC_Time],[Username,UTC_Time],...]
banned_users = ["TheWutBot", "TheWallGrows","AutoModerator", "CantHearYouBot2"] #Other bots and people who hate this bot.
Triggers = ('what', 'wut', 'wat', 'wot','what did you said','wat did u said') #Text that triggers the bot.
no_link_subs = ("ImGoingToHellForThis") #Subs that have asked me not to link to the subreddit
pony_subs = ("mylittlepony", "mlplounge", "clopclop", "ploungeafterdark", "heyitsshugatest") #Subs that are for bronies.
bot_rights = ("botsrights", "botwatch") #Subs that are for people who love bots.

footer = { #text at the end of the post. !normal is the default, !no_link is without links, !pony is for pony subs, !botsrights is for botsrights subs, and the rest are for custom subs
"!normal":"***\n\n##[^^^(I&#32;am&#32;a&#32;bot,&#32;and&#32;I&#32;don't&#32;respond&#32;to&#32;myself.)](https://np.reddit.com/r/"+bot_subreddit+"/)",

"!no_link":"***\n\n^^^(I&#32;am&#32;a&#32;bot,&#32;and&#32;I&#32;don't&#32;respond&#32;to&#32;myself.)",

"totallynotrobots":"***\n\n##[^^^HELLO ^^^FELLOW ^^^HUMANS! ^^^I ^^^AM ^^^A ^^^~~bot~~HUMAN ^^^TOO, ^^^AND ^^^I ^^^DON'T ^^^RESPOND ^^^TO ^^^MYSELF.](https://np.reddit.com/r/"+bot_subreddit+"/)",

"!pony":"***\n\n##[^^^(Hello&#32;everypony!&#32;I&#32;am&#32;a&#32;bot,&#32;and&#32;I&#32;don't&#32;respond&#32;to&#32;myself.)](https://np.reddit.com/r/"+bot_subreddit+"/)",

"!botsrights":"***\n\n##[^^^(Hello&#32;bot&#32;right&#32;activists!I&#32;am&#32;a&#32;bot,&#32;and&#32;I&#32;don't&#32;respond&#32;to&#32;myself.)](https://np.reddit.com/r/"+bot_subreddit+"/)",

"undertale":"***\n\n##[^^^(hOI!!!&#32;iM&#32;A&#32;bOT!&#32;i&#32;dOnT&#32;rESpOND&#32;tO&#32;mYSElF.)](https://np.reddit.com/r/"+bot_subreddit+"/)"
}

def check_condition(c): #The condition for the bot. If this is true, the bot will comment.
    return (c.body.lower().rstrip('?').rstrip('!').rstrip('‽').rstrip('.').rstrip(',').rstrip(';'). in Triggers) and (not RateLimit(str(c.author))) #Is the comment a trigger, and is the author not rate limited. Each .rstrip('‽') adds support to different punctuation.

def bot_action(c,r): #Action the bot preforms
    global users
    parent = r.get_info(thing_id=c.parent_id) #get parent comment

    if str(parent.author) in banned_users or str(c.author) in banned_users: return #If users banned: return

    if isNotAValidComment(parent): return #If it is a response to a thread, stop.
    subreddit = str(c.subreddit)

    if str(parent.author) == username and parent.body != "In da but": #If parent is bot and comment is not "in da but"
        return

    users.append([str(c.author),c.created_utc]) #Add username and time of use to the users list


    if check_condition(parent): #If both comments are triggers, ie. What What
        try:
            c.reply("In da but")
        except:
            pass
        return

    lines = parent.body.split("\n") #Split parent into lines
    total = ""
    for line in lines: #for each line
        pLine = parseLine(line) #Parse line
        total += pLine
    try:
        c.reply(total + get_footer(subreddit))
    except:
        return

def findUsersWithName(name): #find all people with username on the users list
    uses = []
    for use in users: #For each use
        if use[0] == name: #If use name is username
            uses.append(use)
    return uses #Yesus

def getLastTimeOfUse(name): #Get last time a username has used the bot
    return findUsersWithName(name)[-1][1]

def RateLimit(username): #Boolean. if user has used the bot in the last 5 minutes, stop.
    if username == creator_name: return False #unlimited testing
    c_time = time.time() #Current time
    if findUsersWithName(username) == []: #first time using the bot
        return False #No Rate limiting
    lastUseTime = getLastTimeOfUse(username) #Latest time of use
    return (c_time - lastUseTime) <= 300 #has the user used the bot in the last 300 seconds (5 minutes)

def get_footer(subreddit): #gets footer via subreddit name
    ft = ""
    if subreddit in no_link_subs:
        ft = footer["!no_link"]
    elif subreddit in pony_subs:
        ft = footer["!pony"]
    elif subreddit in bots_rights:
        ft = footer["!botsrights"]
    elif subreddit in footer:
        ft = footer[subreddit]
    else:
        ft = footer["!normal"]
    return ft

def parseLine(line): #Written by the awesome sctigercat1
    # Some basic parsing rules that bypass the rest of our logic.
    if line == '' or line == '***': # Restore split newline // Horizontal rule
        return line + '\n'

     #Bold the line
    if line[0] == ">":
       line = ">#" + line[1:]
    elif line[0] != '#':
       line = '#' + line

    # Uppercase the line, all except URLs. Could probably be made more effective?
    ldata = re.split(r"(\[.*?\]\(.*?\))", line) # this finds reddit markdown URLs, i.e. [google](http://google.com)
    line = ''
    for content in ldata:
        if not content.startswith('['): # typical string
            content = content.upper()
        else:
            # url; so let's break it up a little further and capitalize the title also
            url_groups = re.search(r"\[(.*)\]\((.*)\)", content)
            content = '[' + url_groups.group(1).upper() + '](' + url_groups.group(2) + ')'

        line += content

    # Finally, return!
    return line + '\n'

def isNotAValidComment(thing): #Is it not a valid comment
    return hasattr(thing,"domain") #If it has domain, It's a post, so ignore.

#Bot code

r = praw.Reddit(user_agent) #user_agent

r.login(username=username,password=password,disable_warning=True)

for c in praw.helpers.comment_stream(r, 'all'): #for all comments
    if check_condition(c): #If condition
        bot_action(c,r) #Action
