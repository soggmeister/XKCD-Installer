#! python3

import requests, os, sys, shutil, send2trash, re, unidecode, getpass
from bs4 import BeautifulSoup
from os.path import join
from time import sleep

os.system("color F0") # In true XKCD Style, black on white.
print('LOADING...\n')
sleep(1) # For effect :)


##  ACQUIRE THE USERNAME OF CURRENT USER

user = getpass.getuser()

##  CREATE ALL PATHS TO USE IN XKCD UPDATE AND DOWNLOAD

desktopPath = ("C:/Users/%s/Desktop/" % (user))
userXKCDFile = ("C:/Users/%s/Desktop/XKCD" % (user))
userTextFile = ("C:/Users/%s/Desktop/XKCD/XKCD Captions.txt" % (user))
userComicFile = ("C:/Users/%s/Desktop/XKCD/Comics" % (user))

os.chdir(desktopPath)



##  CHECK IF XKCD FILE IS PRESENT, IF NOT, CREATE XKCD, COMICS,
##  AND XKCD CAPTIONS.TXT

if os.path.exists(userXKCDFile) == False :
        print('Making XKCD directory in %s.\n' % (desktopPath))
        os.mkdir(desktopPath + '/XKCD/')
        
if os.path.exists(userComicFile) == False:
        print('Making a Comics folder in %s.\n' % (userXKCDFile))
        os.mkdir(userXKCDFile + '/Comics/')
        
if os.path.exists(userTextFile) == False:
        print('Making "XKCD Captions.txt" in %s.\n' %(userXKCDFile))
        os.chdir(userXKCDFile)
        open("XKCD Captions.txt", "w")


####################################################################################

#  DELETE ALL EXISTING CONTENT IN BOTH COMICS AND XKCD CAPTIONS.TXT.


while True:
        print('Please enter Y if you wish to clear your XKCD Repository. Otherwise, enter N.\n')
        requestDelete = input()
        if requestDelete.lower() == 'y':
                    print('\nARE YOU SURE? Y/N?')
                    requestDelete = input().upper()
                    if requestDelete == 'Y':
                        os.chdir(userComicFile)
                        open(userTextFile, 'w').close()
                        for root, dirs, files in os.walk(userComicFile):
                                print('\nCURRENT FILES BEING CLEARED...\n')
                                for f in files:
                                        os.remove(os.path.join(root, f))
                                for d in dirs:
                                        send2trash.send2trash(os.path.join(root, d))
                        break
        elif requestDelete.lower() == 'n':
                print('XKCD repostiory retained.')
                break
        else:
                print('\n%s is an invalid input.\n' % (requestDelete))
                continue


####################################################################################

##  ACQUIRE THE LyATEST OWNED XKCD ISSUE FROM USER FILES
        
latestOwned = 0
latestFileRegex = re.compile(r'\[\d{1,4}\]')
digitRegex = re.compile(r'\d{1,1000}') # prior to 2019-09-12 20:20, re.compile(r'\d{1,100}')

os.chdir(userXKCDFile)
for folderName, subfolders, filenames in os.walk(os.getcwd()):
        fileOfEditions = latestFileRegex.findall(str(filenames))
        for i in fileOfEditions:
                edition = digitRegex.search(i)
                edition = int(edition.group())
                if edition > latestOwned:
                        latestOwned = edition
        
                
##print(type(latestOwned))  # integer
##print(latestOwned)        # latest owned issue

## ACQUIRE LATEST XKCD COMIC ID FROM XKCD WEBSITE

# Authors note. This code scans through the entirety of the website's code.
# In one section of the HTML's head, a meta tag has a content with the link for
# XKCD's newest comic. This is conveinient! Despite just typing in 'xkcd.com', we can find
# the newest edition regardless of the fact. Hurray brilliant web design!

comicPage = requests.get('https://xkcd.com/')
html = BeautifulSoup(comicPage.content, features="lxml")
latestSeeker = html.get_text()
linkRegex = re.compile(r'\w{3,5}://xkcd.com/\d{4}')
latestLink = linkRegex.findall(latestSeeker)
latestXKCD = digitRegex.search(str(latestLink))
latestXKCD = int(latestXKCD.group())
os.chdir(userComicFile)

##  DOWNLOAD NOT REQUIRED BECAUSE LATEST ISSUES ALREADY DOWNLOADED

if(latestOwned == latestXKCD):
        print('\nYou already have the latest issues of XKCD comics and captions.')
        os.system("@pause")
        os.startfile(userComicFile)
        os.startfile(userTextFile)
        sys.exit()

##print(type(latestXKCD))  # integer
##print(latestXKCD)        # latest XKCD issue + 1


print('XKCD DOWNLOAD INTIATING! :D\nUPLOADING TO ' + os.getcwd() + '.\n\n' +
      'Starting from comic: ' + '[' + str(latestOwned + 1) + '].\n')

#  LOOP THROUGH ALL XKCD COMICS

for i in range(latestOwned + 1, latestXKCD + 1):
    if i == 404:
        os.chdir(userXKCDFile)
        caption = open('XKCD Captions.txt', 'a')
        caption.write(str([i]) + ' XKCD\'s 404 Page. Literally... nginx was here\n')
        caption.close()
        continue
    #  RESET CWD, TURN HTML INTO BEAUTIFUL SOUP
    
    os.chdir(userComicFile)
    comicPage = requests.get('https://xkcd.com/' + str(i) + '/')
    html = BeautifulSoup(comicPage.content, features="lxml")
    #  GET ALL NAMES

    name = html.select('#ctitle')
    name = name[0].text
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = unidecode.unidecode(name)
    
    #  ACQUIRE ALL THE IMG TITLES

    try:
        title = html.select('#comic > img')
        if title == []:
                title = html.select('#comic > a > img')
        title = title[0].get('title')
        title = unidecode.unidecode(title)
        
    except:
        print('Comic [%s] was unsucessfully downloaded. It is either interactive or has a cursed title.\n' % (i))
        os.chdir(userXKCDFile)
        caption = open('XKCD Captions.txt', 'a')
        caption.write(str([i]) + ' Name: ' + name + ' [INTERACTIVE or CURSED TITLE]\n')
        caption.close()
        continue

    #  GET ALL URLS

    url = html.select('#comic > img')
    if url == []:
             url = html.select('#comic > a > img')
    url = 'https:' + url[0].get('src')
    
    #  IMPORT TO COMICS FILE

    img = requests.get(url, stream=True)
    with open(str([i]) + ' ' + name + '.png', 'wb') as out_file:
        shutil.copyfileobj(img.raw, out_file)
    del img

    #  IMPORT ALL ALT TITLE TO TEXT FILE

    os.chdir(userXKCDFile)
    caption = open('XKCD Captions.txt', 'a')
    caption.write(str([i]) + ' ' + title + '\n')
    caption.close()

print('ALL XKCD COMICS AND ALT TITLES HAVE BEEN DOWNLOADED.')
os.system("@pause")
os.startfile(userComicFile)
os.startfile(userTextFile)
sys.exit()

    




