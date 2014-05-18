'''
Created on Sep 7, 2013

@author: anuvrat
'''
import pickle
from datetime import datetime
import urllib.request
from bs4 import BeautifulSoup
import re
import string
import json
import codecs
import sys
import os
import random
print("here");
def loadState():
    print("loadState")
    try:
        state_file = open( "itunes_store_state_dump_try_a.pba", "rb" )
        apps_discovered = pickle.load( state_file )
        print("bgrjbrjbiwr");
        apps_pending = pickle.load( state_file )
        state_file.close()
        print( "Pending = ", len( apps_pending ), " Discovered = ", len( apps_discovered ) )
        return apps_discovered, apps_pending
    except IOError:
        print( "A fresh start ..." )
        return [], []

character_encoding = 'utf-8'
apps_discovered, apps_pending = loadState()
count_offset = len( apps_discovered )
apps_categories = {}

start_time = datetime.now()

def getPageAsSoup( url ):
    print("getPageAsSoup")
    try:
        response = urllib.request.urlopen( url )
    except:
    	return None
    #except urllib.error.HTTPError as e:
    #    print( "HTTPError with: ", url, e )
    #    return None
    #except urllib.URLError as e:
    #	return None
    the_page = response.read()
    soup = BeautifulSoup( the_page )

    return soup

def reportProgress():
    print("reportProgress")
    current_time = datetime.now()
    elapsed = current_time - start_time
    v = ( ( len( apps_discovered ) - count_offset ) / elapsed.seconds ) * 60
    t = len( apps_pending ) / v if v > 0 else 0
    print( "Pending = ", len( apps_pending ), " Discovered = ", len( apps_discovered ), " Velocity = ", str( v ), " parsed per min and Time remaining in min = ", str( t ) )
    print( json.dumps( apps_categories ) )

def saveState():
    print("saveState")
    state_file = open( "itunes_store_state_dump_try_a.pba", "wb" )
    pickle.dump( apps_discovered, state_file )
    pickle.dump( apps_pending, state_file )
    state_file.close()
    reportProgress()

def getApps( categoryUrl ):
    print("getApps")
    print(categoryUrl)
    previous_apps = []
    start_idx = 1
    herecnt =0
    while( True ):
        #if herecnt == 10:
        #	break
        url = categoryUrl + "&page=" + str( start_idx )
        print( url )
        categoryPage = getPageAsSoup( url )
        allAppLinks = [aDiv.get( 'href' ) for aDiv in categoryPage.findAll( 'a', href = re.compile( '^https://itunes.apple.com/in/app' ) )]
        if allAppLinks == previous_apps: break
        apps_pending.extend( [appLink for appLink in allAppLinks if appLink not in apps_pending] )
        previous_apps = allAppLinks
        start_idx += 1
        herecnt = herecnt + 1
    saveState()

def getAppDetails( appUrl ):
    print("getAppDetails")
    if appUrl in apps_discovered: return None
    soup = getPageAsSoup( appUrl )
    if not soup: return None

    pTitleDiv = soup.find( 'p', {'class' : 'title'} )
    if pTitleDiv and pTitleDiv.getText() == 'One Moment Please.': return None

    appDetails = {}
    appDetails['app_url'] = appUrl
    
    titleDiv = soup.find( 'div', {'class' : 'product-review'} )
    print(titleDiv)
    appDetails['description'] = titleDiv.find( 'p' ).getText()
    print(appDetails['description'])
    print(appUrl)
    
    titleDiv = soup.find( 'div', {'id' : 'title'} )
    print(titleDiv)
    heretitle = titleDiv.find('h1').getText()
    for character in heretitle:
      if character in string.punctuation:
         heretitle = heretitle.replace(character, " ")
         
    appDetails['title'] = heretitle #titleDiv.find( 'h1' ).getText()
    appDetails['developer'] = titleDiv.find( 'h2' ).getText()
    
    detailsDiv = soup.find( 'div', {'id' : 'left-stack'} )
    if not detailsDiv: return None

    priceDiv = detailsDiv.find( 'div', {'class' : 'price'} )
    if priceDiv: appDetails['price'] = priceDiv.getText()
    else:
    	appDetails['price'] = "None"

    categoryDiv = detailsDiv.find( 'li', {'class' : 'genre'} )
    if categoryDiv: appDetails['category'] = categoryDiv.find( 'a' ).getText()
    else:
    	appDetails['category'] = "None"

    releaseDateDiv = detailsDiv.find( 'li', {'class' : 'release-date'} )
    if releaseDateDiv: appDetails['release_date'] = releaseDateDiv.getText()
    else:
    	appDetails['release_date'] = "None"

    languageDiv = detailsDiv.find( 'li', {'class' : 'language'} )
    if languageDiv: appDetails['language'] = languageDiv.getText().split()
    else:
    	appDetails['language'] = "None"

    contentRatingDiv = detailsDiv.find( 'div', {'class' : 'app-rating'} )
    if contentRatingDiv: appDetails['content_rating'] = contentRatingDiv.getText()

    contentRatingReasonDiv = detailsDiv.find( 'list app-rating-reasons' )
    if contentRatingReasonDiv: appDetails['content_rating_reason'] = [li.getText() for li in contentRatingReasonDiv.findAll( 'li' )]

    compatibilityDiv = detailsDiv.find( 'p' )
    if compatibilityDiv: appDetails['compatibility'] = compatibilityDiv.getText()
    else:
    	appDetails['compatability'] = "None"
		
    customerRatingDivs = detailsDiv.findAll( 'div', {'class' : 'rating', 'role': 'img'} )
    if customerRatingDivs:
        customerRating = customerRatingDivs[-1].get( 'aria-label' ).split( ',' )
        appDetails['rating'] = customerRating[0].strip()
        appDetails['reviewers'] = customerRating[1].strip()
    else:
        appDetails['rating'] = "None"
    appLinksDiv = soup.find( 'div', {'class' : 'app-links'} )
    if appLinksDiv:
        for link in appLinksDiv.findAll( 'a', {'class' : 'see-all'} ):
            text = link.getText()
            href = link.get( 'href' )
            if text.endswith( 'Web Site' ): appDetails['developer_wesite'] = href
            elif text.endswith( 'Support' ): appDetails['support'] = href
            elif text.endswith( 'Agreement' ): appDetails['license'] = href

    apps_discovered.append( appUrl )
    if os.path.isfile(appDetails['title']):
    	return None
    f = open(appDetails['title'], 'w')

    f.write("#Title:\n")
    f.write(''.join(appDetails['title']));

 
    f.write("\n#Compatibility:\n")
    f.write(''.join(appDetails['compatibility']))
   
    f.write("\n#Developer:\n")
    f.write(''.join(appDetails['developer']))
    
    f.write("\n#Description:\n")
    f.write(''.join(appDetails['description']))
    
    f.write("\n#Price:\n")
    f.write(''.join(appDetails['price']))
    
    f.write("\n#Category:\n")
    f.write(''.join(appDetails['category']))

    f.write("\n#ReleaseDate:\n")
    f.write(''.join(appDetails['release_date']))
    
    f.write("\n#Language:\n")
    f.write(''.join(appDetails['language']))
    
    f.write("\n#Rating:\n")
    f.write(''.join(appDetails['rating']))
    f.close()

    return appDetails
    
def closeFileHandlers( fileHandlers ):
    for v in fileHandlers.values():
        v.close()


if __name__ == '__main__':
    itunesStoreUrl = 'https://itunes.apple.com/in/genre/ios/id36?mt=8'
    mainPage = getPageAsSoup( itunesStoreUrl )
    allCategories = []
    
    for column in ['list column first', 'list column', 'list column last']:
        columnDiv = mainPage.find( 'ul', {'class' : column} )
        allCategories.extend( aDiv.get( 'href' ) for aDiv in columnDiv.findAll( 'a', href = re.compile( '^https://itunes.apple.com/in/genre' ) ) )
    cnt = 0;
    ncnt  = 1;
    
    #for category in allCategories: 
    while ncnt < len(allCategories):
        ind = -ncnt
        ncnt = ncnt + 1
        category = allCategories[ind]
        print("here")
        a= category.split("/")
        print(a)
        print(a[-2])
        if os.path.exists(a[-2]):
       		continue;
        cnt = cnt + 1
        for alphabet in string.ascii_uppercase:
        	getApps( category + '&letter=' + alphabet )
        fileHandlers = {}
        count = 100
        newcnt =0
        tot_apps = len(apps_pending)
        to_take = tot_apps
        
        while to_take > 0:
        	to_take = to_take -1
        	if count == 0:
        		saveState()
        		count = 100
        	count = count - 1
        	app = random.choice(apps_pending)
        	apps_pending.remove(app)
        	if not app: continue
        	try:
        		if not os.path.exists(a[-2]):
        			os.makedirs(a[-2])
        		os.chdir(a[-2])
        		app_data = getAppDetails( app )
        		os.chdir("..")
        	except Exception as e:
        		print( app, e )
        		exit( 1 )
        	if not app_data:
        		continue
        	saveState()
        del apps_pending[:]
        #os.chdir("..");
    closeFileHandlers( fileHandlers )	
