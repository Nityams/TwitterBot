# by Nityam Shrestha
# encoding=utf8
import sys
import markovify
import nltk
import random
import tweepy
import time
import PIL
import enchant
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# DEBUG
# text_file = open("Output2.txt", "w")

#---------------- CONSTANTS --------------------------
# system language stuffs
reload(sys)
sys.setdefaultencoding('utf8')

# Tweeter authuntication
CONSUMER_KEY = "123123123123...."     # your authentications here
CONSUMER_SECRET = "123123123123...."     # your authentications here

ACCESS_KEY = "123123123123...."     # your authentications here

ACCESS_SECRET = "123123123123...."     # your authentications here

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# set of colors
lightColors = [(255, 255, 255), (46, 241, 211), (198, 255, 109), (250, 149, 53), (131, 192, 246),
                (255, 138, 255), (255, 241, 0), (0, 255, 255), (218, 165, 32), (204, 255, 255), (255, 204, 204)]

darkColors = [(0, 0, 0), (102, 25, 0), (0, 132, 140), (110, 44, 44), (98, 33, 96),
               (48, 37, 233), (14, 62, 64), (14, 64, 37), (47, 60, 5),  (40, 40, 40), (0, 51, 51)]

font = ImageFont.truetype(
    "/Users/nityamshrestha/Library/Fonts/Lie_to_Me-TTF.ttf", 50)
# fixed charLength
charLength = 140

# set of hashtags
hashtags = ['#inspire', '#boss', '#optimism', '#friends', '#adventure', '#wanderlust', '#nature ', '#beach ', '#culture ', '#memories', ' #journey ',
    '#photography ', '#wander ', '#lost ', '#escape ', '#inspiration ', '#girl ', '#soloif ', '#sacrifice ', '#reading ', '#readingmatters ', '#knowledge ', '#habbits ']
hashtags2 = ['#motivation','motivationalpoems','#life','#beauty','#art','#igdaily','#2017','#quote','#peom','#truth','#enjoy','#creative','#old','#drunk','#hope','#random','#reflection','#custom','#abstract','#literature','#poetry','#artoftheday','#thoughts','#instawriters']

hashtags3 = ['#creativewriting','#picoftheday','#mind','#poetsofinstagram','#instapoetry','#motivationalpoetry','#igpoets','#writersblock','#wordstoliveby','#storyteller','#journalentry','#poemsporn','#deep','#poetryspeakssometimes','#poetryspeaks','#imagination','#arttherapy','#carpediem','#wisewords','#dope']
# enchant to US-english
enchantress = enchant.Dict("en_US")
#----------------------------- Logics and Algorithms -------------------------

# Markov Chains
with open("Quotes.txt") as f:
    text = f.read()
    print "<Nityam-DeBug> Text File successfully retrived"

# Build the model.
text_model = markovify.Text(text)
print "<Nityam-DeBug> Model complete"

# functions to get array of colors


def getLightColors():
    return random.sample(lightColors, 1)[0]


def getDarkColors():
    return random.sample(darkColors, 1)[0]

# function to create and save Picture


def createPicture(line1, line2, line3, line4):
    maxLength = max(len(line2), len(line4))
    colorChoice = random.uniform(0, 1)
    if colorChoice:
        background = getDarkColors()
        textColor = getLightColors()
    else:
        background = getLightColors()
        textColor = getDarkColors()

    # set background:
    if maxLength < 15:
        img = Image.new("RGBA", (410, 360),
                        (background[0], background[1], background[2]))
    elif maxLength < 25:
        img = Image.new("RGBA", (700, 400),
                        (background[0], background[1], background[2]))
    else:
        img = Image.new("RGBA", (1000, 400),
                        (background[0], background[1], background[2]))

    draw = ImageDraw.Draw(img)

    # set text:
    draw.text((50, 20), line1,
              (textColor[0], textColor[1], textColor[2]), font=font)
    draw.text((150, 100), line2,
              (textColor[0], textColor[1], textColor[2]), font=font)
    draw.text((50, 180), line3,
              (textColor[0], textColor[1], textColor[2]), font=font)
    draw.text((150, 260), line4,
              (textColor[0], textColor[1], textColor[2]), font=font)
    draw = ImageDraw.Draw(img)
    draw = ImageDraw.Draw(img)

    img.save("tweet.png")


# Create line
def getPoem():
    # create sentence
    sentence = text_model.make_short_sentence(charLength)

    while(sentence == None or len(sentence) < 50):
        print "<Nityam-DeBug> sentence 'none' found, trying again.."
        sentence = text_model.make_short_sentence(charLength)

    line = sentence.split(" ")
    size = len(line) / 4
    line1 = line[0].title() + " "
    line2 = ""
    line3 = ""
    line4 = ""

    #Creating pattern
    if size <= 4:  # pattern a b c b
        setSonnet = True
        patternC = line[len(line) - size]  # getting the last word of 3rd sentence
    else:
        setSonnet = False # pattern a b a b

    for i in range(1, size):
        line1 += line[i] + " "

    for i in range(size, len(line) / 2):
        line2 += line[i] + " "

    for i in range(len(line) / 2, len(line) - size-1):  #-1
        line3 += line[i] + " "

    for i in range(len(line) - size, len(line)-1):    #-1
        line4 += line[i] + " "

    # get word numbers to rhyme
    end1 = line[size - 1]
    end2 = line[len(line) / 2 - 1]
    end3 = line[len(line) - size - 1]
    end4 = line[len(line) - 1]

    # NLTK functions
    # need to rhym
    def rhyme(inp, level):
         entries = nltk.corpus.cmudict.entries()
         syllables = [(word, syl) for word, syl in entries if word == inp]
         rhymes = []
         for (word, syllable) in syllables:
                 rhymes += [word for word,
                     pron in entries if pron[-level:] == syllable[-level:]]
         return set(rhymes)

    def doTheyRhyme(word1, word2):
      # first, we don'st want to report 'glue' and 'unglue' as rhyming words
      # those kind of rhymes are LAME
      if word1.find(word2) == len(word1) - len(word2):
          return False
      if word2.find(word1) == len(word2) - len(word1):
          return False

      return word1 in rhyme(word2, 2)

    # if they already rhyme, no need to change
    txt3 = end3
    txt4 = end4

    if doTheyRhyme(end1,end3) == False:
        rhymeSet = rhyme(end1, 2)
        if len(rhymeSet) > 1:
            end3 = random.sample(rhymeSet,1)
            txt3 = end3.pop()
            counter = 1
            while (enchantress.check(txt3)==False or doTheyRhyme(end1, txt3)== False):
                print 'enchantress3 working: ', txt3
                end3 = random.sample(rhymeSet,1)
                txt3 = end3.pop()
                counter +=1
                if counter >=50:
                    txt3 = end1
                    break


    if doTheyRhyme(end2,end4)== False:
        rhymeSet = rhyme(end2, 2)
        if len(rhymeSet) > 1:
            end4 = random.sample(rhymeSet,1)
            txt4 = end4.pop()
            counter = 1
            while (enchantress.check(txt4) == False or doTheyRhyme(end2, txt4) == False):
                print 'enchantress4 working: ', txt4
                end4 = random.sample(rhymeSet,1)
                txt4 = end4.pop()
                counter +=1
                if counter >=50:
                    txt4 = end2
                    break

    # statement to follow the rhyming pattern
    if setSonnet:
        line3 += patternC     # Pattern: a b c b
    else:
        line3 += txt3         # Pattern: a b a b
   
    line4 += txt4
   
    createPicture(line1, line2, line3, line4)


    # return status #should retrun hashtags

i =0;
while 1:
    myStatus = random.sample(hashtags,1)[0] + '\n' + random.sample(hashtags2,1)[0]+'\n'+ random.sample(hashtags3,1)[0] +'\n' +"#drunk"
    getPoem()
    i+=1
    print 'status no:- ', i
    api.update_with_media("tweet.png",myStatus)
    print '\n'
    time.sleep(900) # will sleep for 900 seconds
