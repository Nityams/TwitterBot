import urllib2, time
from sets import Set

# Auto pulls quotes to Txt file

finalQuotes = ""
text_file = open("Quotes.txt","w")
quoteSets = set()

for num in range(0,1000):
    url ="http://api.forismatic.com/api/1.0/?method=getQuote&format=text&lang=en"
    usock = urllib2.urlopen(url)
    quote=""
    for line in usock:
        quote+=line
    quote = quote.lower()
    quoteSplit = quote.split(' (')
    mainQuote = quoteSplit[0]
    mainQuote += "\n"
    quoteSets.add(mainQuote)
    # text_file.write(mainQuote +"\n")
    time.sleep(2)

for line in quoteSets:
    text_file.write(line)

text_file.close
