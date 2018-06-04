import discord, logging, json
from discord.ext import commands
import random #Necessary for RNG.
import datetime #Necessary to determine current date.
import threading #Necessary to run bdayCheck() function on the side.
import mwclient #Necessary for MediaWiki API.
import sys #Necessary for reasons. Shut up.
import time #Duh.
import os #Duhooo.
import imgurpython #Required for Cool Kids pictures.
import sqlite3 #Required for database management.
from operator import itemgetter #Used to sort list of lists, like in the triviaTracker() function.

"""PRECLUSIVES"""
description = '''The official discord bot of the Beika Street Irregulars.'''
bot = commands.Bot(command_prefix='!bb ', description=description)
client_id = 'CLIENTID'
client_secret = 'CLIENTSECRET'
notebase = sqlite3.connect('D:\\[X] Vault\\[X] Projects\\Blue Book Bot\\DATA\\notebase.db') #Setting up database connection.
curNote = notebase.cursor()
database = sqlite3.connect('D:\\[X] Vault\\[X] Projects\\Blue Book Bot\\DATA\\database.db') #Setting up database connection.
curData = database.cursor()
triviabase = sqlite3.connect('D:\\[X] Vault\\[X] Projects\\Blue Book Bot\\DATA\\triviabase.db') #Setting up triviabase connection.
curTriv = triviabase.cursor()
system = sqlite3.connect('D:\\[X] Vault\\[X] Projects\\Blue Book Bot\\DATA\\system.db') #Setting up system connection.
curSys = system.cursor()
trivState = 0
trivAns = ''

"""DEFAULT SERVER ARRAYS"""
roleIDs = { #Global role ID dictionary for easy reference.
        'admin' : 346072731562803200,
        'mod' : 346072731562803200,
        'scans' : 346072806230065154
        }
adminIDs = { #All admin user IDs.
        126473945787531264 : 'N',
        298534899340804098 : 'Baka',
        225716785658200065 : 'Chem',
        256120280458461184 : 'Wyz',
        205123331731619840 : 'Yun',
        }
channelIDs = { #Global channel ID dictionary for easy reference.
        'admin' : '266158714774487040',
        'announcements' : '273561781610348545',
        'roleplay' : '298588910009712640',
        'bots_voicechat' : '266149598312136704'
        }
authorizedPersonnel = [ #List of User IDs with elevated privileges.
    217405891383787521,
    205123331731619840,
    244710537848422400,
    143704228240556032,
    225832956227354625,
    107692630065840128,
    265630979350200322,
    126473945787531264
    ]

"""DEFAULT ARRAYS"""
curConfig = { #Global config dictionary.
        'Trivia' : 0, #If 1, users can play trivia.
        'Birthday' : 0, #If 1, the bot keeps track of time and announces birthdays.
        'newFlair' : 0, #If 1, new users are auto-flaired.
        'bdayLvl' : 0 #If 0, PMs user. If 1, mentions user in #announcements. If 2, tags @everyone in #announcements.
        }
errorCodes = [ #Ever felt too lazy to do actual work, but too guilty to just not do anything? Yeah, that's how this happened.
    'Don\'t look at me like that. Machines don\'t make mistakes - humans do!',
    'Guess Neuro\'s programming ability isn\'t the only thing that\'s broken. :smirk:',
    'OH DEAR GOD, WHAT DID YOU D-... Actually, that one might have been my fault...',
    'Pobody\'s nerfect. Except Yunnie. :blue_heart:',
    'That\'s what happens when you don\'t feed your coders.',
    'Was Neuro on a rice diet when he wrote this?',
    'No funny error message here. Just mistery and failure.',
    'That typo was uglier than Kirro\'s face. HAH!',
    'I\'m starting to run out of error messages...',
    'Ain\'t no bot like a Neuro bot \'cause a Neuro bot don\'t work. ♪',
    '`THIS ERROR MESSAGE HAS BEEN REPLACED BY A COMMERCIAL FOR AXE BODY SPRAY. WEAR IT, YOU STINK.`',
    'God is dead. Life is pain. Existence is misery.','Life is existence. Existence is god. Misery.',
    'Let\'s just agree that we both messed up and leave it at that.',
    'There are more bugs in this code than spies in the B.O. *Ba dum tss.*',
    'This is bad. Let\'s panic and annoy our code monkey! Hey, <@126473945787531264>, get over here!'
    ]
encourageEm = [ #I disappoint myself.
    'At \'em, Tiger!',
    '[N] may be the King, but you\'re not half bad!',
    'You better not be cheating! :thinking:'
    'That... was pretty good.',
    'I was sure you wouldn\'t get this one...',
    'Just as expected of a detective otaku.',
    'Something special might happen if you win a lot of trivia games...'
    ]
funFacts = [ #Might as well go all out, I guess.
    'Neuro is in love.',
    'This bot is running on 4 servers.',
    'Yunnie is the greatest girlfriend a guy could wish for. <3',
    'Neuro\'s Steam ID is `9696261`.',
    'Neuro reads Hagrid with a scottish accent.',
    'Nobody exists on purpose. Nobody belongs anywhere. We\'re all going to die.',
    'Life holds no meaning beyond the one we (often arbitrarily) assign to it.',
    'It is only through labor and painful effort, by grim energy and resolute courage, that we move on to better things.',
    'All our knowledge merely helps us to die a more painful death than animals that know nothing.',
    'I love Yun','We are all alone.',
    'There is no god.',
    'Current Record: 186.',
    'Robots are cool.',
    'Try the `!bb shinran` command sometime.',
    'The bot has some fun secret commands, as well as clues hinting towards them strewn around. Try to find them all!'
    ]
evilMen = [ #Might as well go all out, I guess.
    'You are a colossal fool.',
    'Hey <@126473945787531264>, come laugh at this loser!',
    'Let\'s be honest, this is far from your greatest failure thus far.',
    'Your mother would be disappointed if she hadn\'t given up on you years ago.',
    'The inner machinations of my mind lay undetected!',
    'Abandon all curiosity ye who enter here.',
    'No cigar. Not even close. You suck.',
    'This is why you will die alone.',
    'I get that this is the only way for you to feel some degree of fulfillment, but you need to accept the fact that you\'re just not meant to be happy.',
    'You are literally the single worst person ever to attempt this.',
    'You\'re ugly, we\'re all just too nice to say it.',
    'Your birth was payback for the sins of man.',
    'You are the epitome of all that is wrong with this world.',
    'I honestly just hate you.',
    'Nope.',
    'https://www.tenor.co/Um8v.gif',
    'https://www.tenor.co/tGt0.gif',
    'https://www.tenor.co/J7yw.gif',
    'https://www.tenor.co/qfHD.gif',
    ]
timezones = { #Global timezone dictionary.
    'GMT' : '383821824812908545',
    'GMT+1' : '383822281291464706',
    'GMT+2' : '383822365248978945',
    'GMT+3' : '383822454595780610',
    'GMT+4' : '383822508488654848',
    'GMT+5' : '383822562393849857',
    'GMT+5:30' : '440109967681519616',
    'GMT+6' : '383822623684952077',
    'GMT+7' : '383822676424261644',
    'GMT+8' : '383822863360327700',
    'GMT+9' : '383822920624898068',
    'GMT+9:30' : '440121261369327618',
    'GMT+10' : '383822977940062214',
    'GMT+11' : '383823039751520267',
    'GMT-1' : '383823161084477440',
    'GMT-2' : '383823247763832834',
    'GMT-3' : '383823307084136449',
    'GMT-4' : '383823373786021888',
    'GMT-5' : '383823432615460875',
    'GMT-6' : '383823495148208130',
    'GMT-7' : '383823640002822144',
    'GMT-8' : '383823706532610048',
    'GMT-9' : '383823765307654145',
    'GMT-10' : '383823827034963968',
    'GMT-11' : '383823897168052224',
    'GMT+12' : '440107610520158209',
    }
triviaPlayers = { #Global registry of current trivia players.
    }
charChans = { #Global registry of current trivia players.
    'Shinichi' : '412616085196636160',
    'Conan' : '412616085196636160',
    'Shiho' : '412602249584312341',
    'Haibara' : '412602249584312341',
    'Hakuba' : '413145561974439937',
    'Sonoko' : '412645346158706690',
    'Kogoro' : '413699778573107200',
    'Amuro' : '412601928539701257',
    'Kaito' : '412785456267395072',
    'Akai' : '412601993979363328',
    'Ran' : '412609822429544458',
    }

"""SYSTEM FUNCTIONS"""
def validateAdmin(userID): #Verifies that a user is an admin.
    for eachAdmin in adminIDs:
        print (eachAdmin)
        if userID == eachAdmin:
            return (True)
    return (False)
def funFact(): #What? I'm allowed to procrastinate...
    return funFacts[random.randint(0,len(funFacts)-1)]
def evilMan(): #What? I'm allowed to procrastinate...
    return evilMen[random.randint(0,len(evilMen)-1)]

"""CORE FUNCTIONS"""
def notification(action,content): #Handles game notification requests.
    tempMem = []
    tempMem01 = ''
    if action == 'start':
        content = content[15:]
        curNote.execute("CREATE TABLE {name} (UserID INTEGER PRIMARY KEY);".format(name=content))
        notebase.commit()
        return('Game has been added!')
    elif action == 'subscribe':
        content = content[12:]
        intel = content.split(' /// ')
        curNote.execute("INSERT INTO {name} (UserID) VALUES ({ID})".format(name=intel[0],ID=intel[1]))
        notebase.commit()
        return('User has been subscribed!')
    elif action == 'notify':
        content = content[15:]
        curNote.execute("SELECT * FROM {name}".format(name=content))
        rows = curNote.fetchall()
        listing = []
        print(rows)
        for everyEntry in rows:
            listing += everyEntry
        print (listing)
        finale = ""
        for everyEntry in listing:
            finale = finale + ("<@" + str(everyEntry) + ">\n")
        print(finale)
        return(finale)
    elif action == 'summary':
        res = notebase.execute("SELECT name FROM sqlite_master WHERE type='table';")
        listing = []
        finale = ""
        for name in res:
            listing += name
        print(listing)
        for everyEntry in listing:
            finale = finale + ("► " + str(everyEntry) + "\n")
        return(finale)
    elif action == 'unsub':
        content = content[15:]
        intel = content.split(' /// ')
        curNote.execute("DELETE FROM {name} WHERE UserID={ID}".format(name=intel[0],ID=intel[1]))
        notebase.commit()
        return('User has been unsubscribed!')
def trivia(action,type):
    if action == 'start':
        trivset = curTriv.execute("SELECT * FROM {name} WHERE id IN (SELECT id FROM {name} ORDER BY RANDOM() LIMIT x)".format(name=type))
        print(trivset)

# Print the starting text
print('\nLoading BSI Bot...')
print('Please Wait...\n')

# Setup basic logging for the bot
logging.basicConfig(level=logging.WARNING)

@bot.event
async def on_ready():
    print('The BSI Bot is operational.')

@bot.command(pass_context=True)
async def credit(context):
    credEmbed = discord.Embed(title='Beika Street Bot - Credits', description='Beika Street Bot was written by <@126473945787531264>.\nFind more BSI works at `www.beikastreet.net`.', colour=0xDEADBF)
    credEmbed.set_author(name='Fun Fact: ' + funFact())
    await bot.send_message(context.message.channel,  embed=credEmbed)

@bot.group(pass_context=True)
async def note(context):
    if context.invoked_subcommand is None:
        await bot.say('Invalid sub-command. Contact <@126473945787531264>.')

@note.command(pass_context=True)
async def spawn(context):
    await bot.send_message(context.message.channel,  notification('start',context.message.content))

@note.command(pass_context=True)
async def sub(context):
    await bot.send_message(context.message.channel,  notification('subscribe',context.message.content + ' /// ' + context.message.author.id))

@note.command(pass_context=True)
async def unsub(context):
    await bot.send_message(context.message.channel,  notification('unsub',context.message.content + ' /// ' + context.message.author.id))

@note.command(pass_context=True)
async def alert(context):
    await bot.send_message(context.message.channel, "**NOTIFYING \"" + context.message.content[15:] + "\" SUBSCRIBERS.**\n" + notification('notify',context.message.content))

@note.command(pass_context=True)
async def index(context):
    await bot.send_message(context.message.channel, "**GROUP INDEX:**\n" + notification('summary',context.message.content))

@bot.group(pass_context=True)
async def time(context):
    print (context.message.content)
    print (context.message.content[9:])
    if context.message.content[9:].startswith('GMT') == True:
        await bot.add_roles(context.message.author, discord.Object(id=timezones[context.message.content[9:]]))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'EST':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT-5']))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'PST':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT-8']))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'BST':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT+1']))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'MSK':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT+3']))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'SGT':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT+8']))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'IST':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT+5:30']))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'CEST':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT+2']))
        await bot.send_message(context.message.channel, "Flair added.")
    elif context.message.content[9:] == 'AEST':
        await bot.add_roles(context.message.author, discord.Object(id=timezones['GMT+9:30']))
        await bot.send_message(context.message.channel, "Flair added.")

@bot.group(pass_context=True)
async def play(context):
    if context.invoked_subcommand is None:
        await bot.say('Invalid sub-command. Contact <@126473945787531264>.')

@play.command(pass_context=True)
async def roll(context):
    await bot.send_message(context.message.channel,  'You rolled `' + str(random.randint(0,100)) + "`.")

@play.command(pass_context=True)
async def countdown(context):
    if context.message.channel[19:] == "":
        await bot.send_message(context.message.channel,  'You rolled `' + str(random.randint(0,100)) + "`.")

@play.command(pass_context=True)
async def coin(context):
    if random.randint(0,100) % 2 == 0:
        await bot.send_message(context.message.channel,  'The result of the coin flip was `heads`.')
    else:
        await bot.send_message(context.message.channel,  'The result of the coin flip was `tails`.')

@bot.group(pass_context=True)
async def trivia(context):
    if context.invoked_subcommand is None:
        await bot.say('Invalid sub-command. Contact <@126473945787531264>.')

@trivia.command(pass_context=True)
async def start(context):
    if context.message.content.startswith("case") == True:
        if trivState == 0:
            trivState = 1
            await bot.send_message(context.message.channel, embed=trivia(start,case))
        else:
            await bot.send_message(context.message.channel, "Sorry, but a trivia game is already going on.")
    elif context.message.content.startswith("general") == True:
        if trivState == 0:
            trivState = 2
            await bot.send_message(context.message.channel, embed=trivia(start,general))
        else:
            await bot.send_message(context.message.channel, "Sorry, but a trivia game is already going on.")

@trivia.command(pass_context=True)
async def score(context):
    await bot.send_message(context.message.channel, trivia(score))

@trivia.command(pass_context=True)
async def answer(context):
    await bot.send_message(context.message.channel, trivia(score))

@trivia.command(pass_context=True)
async def leaderboard(context):
    await bot.send_message(context.message.channel, trivia(leaderboard))

@trivia.command(pass_context=True)
async def skip(context):
    if trivState == 1:
        await bot.send_message(context.message.channel, embed=trivia(skip,case))
    elif trivState == 2:
        await bot.send_message(context.message.channel, embed=trivia(skip,general))

@trivia.command(pass_context=True)
async def quit(context):
    if trivState != 0:
        trivState = 0
        pastQue = []
        await bot.send_message(context.message.channel, '**Scores:**\n')
        for everyEntry in triviaPlayers:
            tempMem1 = everyEntry
            tempMem2 = triviaPlayers[everyEntry]
            await bot.send_message(context.message.channel, str(tempMem1) + ": " + str(tempMem2))
            triviaPlayers[everyEntry] = 0
        triviaPlayers = {}
    else:
        await bot.send_message(context.message.channel, "What now? There's no trivia game going on! You just embarrassed yourself, bud.")

@bot.command(pass_context=True)
async def invite(context):
    await bot.send_message(context.message.channel,"Your invite URL is `https://discord.gg/7uvsFHf`.")

@bot.command(pass_context=True)
async def map(context):
    await bot.send_message(context.message.channel,"**Server Map:**\n`https://www.zeemaps.com/map?group=2452942`.")

@bot.command(pass_context=True)
async def secret(context):
    if context.message.content[11:] == "blue book":
        await bot.send_message(context.message.channel,"https://i.imgur.com/VpisvFa.png")
    elif context.message.content[11:] == "bsi":
        await bot.send_message(context.message.channel,"https://i.imgur.com/8BjMUwl.png")
    elif context.message.content[11:] == "eisuke":
        await bot.send_message(context.message.channel,"https://i.imgur.com/4mj3blq.jpg")
    elif context.message.content[11:] == "best boy":
        await bot.send_message(context.message.channel,"https://i.imgur.com/Y72p09w.png")
    elif context.message.content[11:] == "best girl":
        await bot.send_message(context.message.channel,"https://i.imgur.com/Eowfzu8.png")
    elif context.message.content[11:] == "nike":
        await bot.send_message(context.message.channel,"Fuck off, Nike.")
    elif context.message.content[11:] == "n opinion nike":
        await bot.send_message(context.message.channel,"Not even worth the effort. Seriously, he probably wants a paragraph on his own, but I'm too lazy to bother.")
    elif context.message.content[11:] == "n opinion wyz":
        await bot.send_message(context.message.channel,"Clever, but her focus is too narrow and her vision too person and uninspired to fit the intellectual image she likes to paint whenever given a chance to express herself. Well-meaning but ultimately generic beyond that.")
    elif context.message.content[11:] == "n opinion zero":
        await bot.send_message(context.message.channel,"Surprisingly fun, far more liberated than I'd first expected, but still ultimately dragged down by his own mediocrity. Fun, but lacking in vision and skills alike.")
    elif context.message.content[11:] == "n opinion jin":
        await bot.send_message(context.message.channel,"The worst of humanity, in my mind - clever to enough to feign intellect, wise enough to know better, but too primitive and uninspired to rise beyond mediocrity. Far too resigned to wasting away, lacking in drive and appeal, generally a failure.")
    elif context.message.content[11:] == "n opinion greenglasses":
        await bot.send_message(context.message.channel,"Boring, uninteresting person. Only features of note are her perceived lack of self-actualization and her tendency to knowingly act irrational. Pathetic in many ways.")
    elif context.message.content[11:] == "n opinion yun":
        await bot.send_message(context.message.channel,"https://www.youtube.com/watch?v=rc2jsjnt-HY")
    elif context.message.content[11:] == "n opinion chem":
        await bot.send_message(context.message.channel,"Chocolate adonis with enough sass to rival Louisiana grannies. Good friend, better cake eater.")
    elif context.message.content[11:] == "n opinion m8":
        await bot.send_message(context.message.channel,"Had plenty of potential before Komeileen ruined him. Maybe Mao can save him?")
    elif context.message.content[11:].startswith("n opinion ") == True and context.message.content[11:] != "n opinion m8" and context.message.content[11:] != "n opinion chem" and context.message.content[11:] != "n opinion yun" and context.message.content[11:] != "n opinion greenglasses" and context.message.content[11:] != "n opinion jin" and context.message.content[11:] != "n opinion zero" and context.message.content[11:] != "n opinion wyz" and context.message.content[11:] != "n opinion nike":
        await bot.send_message(context.message.channel,"Wrong secret code - not all of the N Opinion codes start like this. Good luck figuring it out.")
    elif context.message.content[11:] == "greenglasses":
        await bot.send_message(context.message.channel,"https://media.giphy.com/media/3o7btPad6GMQn3NImQ/giphy.gif")
    elif context.message.content[11:] == "amuro":
        await bot.send_message(context.message.channel,"Can you just shut up already?")
    elif context.message.content[11:] == "relax":
        await bot.send_message(context.message.channel,"https://i.imgur.com/4Jc7O0x.mp4")
    else:
        await bot.send_message(context.message.channel,evilMan())

@bot.command(pass_context=True)
async def quit(context):
    if context.message.author.id == 'OWNERID':
        exit()
    else:
        await bot.send_message(context.message.channel,evilMan())

if __name__ == '__main__':
	bot.run('TOKEN')
