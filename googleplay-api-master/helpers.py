from config import SEPARATOR
import urllib2
from BeautifulSoup import BeautifulSoup
import os as ch

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def print_header_line():
    l = [ "Title",
                "Package name",
                "Creator",
                "Super Dev",
                "Price",
                "Offer Type",
                "Version Code",
                "Size",
                "Rating",
                "Num Downloads",
             ]
    print SEPARATOR.join(l)

def print_result_line(c,search):
    #c.offer[0].micros/1000000.0
    #c.offer[0].currencyCode
    #if (c.title=="WhatsApp Messenger"):
    cw = ch.getcwd()
    print cw
    print ch.getcwd()
    print c.title
    print search
    #sys.exit(0)
    ch.chdir('data/'+search)
    f = open(c.docid,'w')
    f.write('#Title:\n')
    f.write(c.title.encode('utf-8'))

    print 'https://play.google.com/store/apps/details?id='+c.docid
    responseu = urllib2.urlopen('https://play.google.com/store/apps/details?id='+c.docid)
    parsed_html = BeautifulSoup(responseu.read())
#    print parsed_html
    reviews= parsed_html.body.findAll('div',attrs={'class':'review-body'})
    print len(reviews)
    ch.chdir(cw)
    ch.chdir("reviews")
    ch.mkdir(c.docid)
    ch.chdir(c.docid)

    for r in range(0,len(reviews)):
        maneet = open("review"+str(r),'w')
        print parsed_html.body.findAll('div',attrs={'class':'review-body'})[r].text
        maneet.write(parsed_html.body.findAll('div',attrs={'class':'review-body'})[r].text.encode('utf-8'))
        maneet.close()

    print len(reviews)
    
   # sys.exit(0)
    boo = parsed_html.body.find('div',attrs={'class':'show-more-content text-body'}).text
    category = parsed_html.body.find('span',attrs={'itemprop':'genre'}).text

    f.write('\n#Developer:\n')
    
    f.write(c.creator.encode('utf-8'))
    f.write('\n#Description:\n')
    
    f.write(boo.encode('utf-8'))
    f.write('\n#Rating:\n')
    
    f.write("%.2f" % c.aggregateRating.starRating)
   
    f.write('\n#Category:\n')
    
    f.write(category.encode('utf-8'))
   
    f.close()
    ch.chdir(cw)
    print c.docid
    
      #sys.exit(0)
    print responseu.read()

    l = [ c.title,
                c.docid,
                c.creator,
                len(c.annotations.badgeForCreator), # Is Super Developer?
                c.offer[0].formattedAmount,
                c.offer[0].offerType,
                c.details.appDetails.versionCode,
                sizeof_fmt(c.details.appDetails.installationSize),
                "%.2f" % c.aggregateRating.starRating,
                c.details.appDetails.numDownloads]
    print SEPARATOR.join(unicode(i).encode('utf8') for i in l)

