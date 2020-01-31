#! python3

######
#
# Special thanks to u/CraigularB for letting me know about the JSON interface.
# Bunch of new additions added and install time dramatically reduced because of his advice. :]
#
######

import requests, os, sys, shutil, send2trash, re, unidecode, getpass, json
from os.path import join

os.system("color F0") # In true XKCD Style, black on white, white under black.

##  ACQUIRE THE USERNAME OF CURRENT USER

user = getpass.getuser()

##  CREATE ALL PATHS TO USE IN XKCD UPDATE AND DOWNLOAD

desktopPath = ("C:/Users/%s/Desktop/" % (user))
userXKCDFile = ("C:/Users/%s/Desktop/XKCD" % (user))
userTextFile = ("C:/Users/%s/Desktop/XKCD/_XKCD Metadata.txt" % (user))
userComicFile = ("C:/Users/%s/Desktop/XKCD/Comics" % (user))
userAltFile = ("C:/Users/%s/Desktop/XKCD/XKCD Alt Titles Only.txt" % (user))
userTranscriptFile = ("C:/Users/%s/Desktop/XKCD/XKCD Transcripts Only.txt" % (user))

os.chdir(desktopPath)

##  CHECK IF XKCD FILE IS PRESENT, IF NOT, CREATE XKCD, COMICS,
##  AND XKCD Metadata.TXT

if os.path.exists(userXKCDFile) == False :
        print('Making XKCD directory in %s.\n' % (desktopPath))
        os.mkdir(desktopPath + '/XKCD/')
        
if os.path.exists(userComicFile) == False:
        print('Making a Comics folder in %s.\n' % (userXKCDFile))
        os.mkdir(userXKCDFile + '/Comics/')
        
if os.path.exists(userTextFile) == False:
        print('Making "_XKCD Metadata.txt" in %s.\n' %(userXKCDFile))
        os.chdir(userXKCDFile)
        open("_XKCD Metadata.txt", "w")
        
if os.path.exists(userAltFile) == False:
        print('Making "XKCD Alt Title Only.txt" in %s.\n' %(userXKCDFile))
        os.chdir(userXKCDFile)
        open("XKCD Alt Titles Only.txt", "w")

if os.path.exists(userTranscriptFile) == False:
        print('Making "XKCD Transcripts Only.txt" in %s.\n' %(userXKCDFile))
        os.chdir(userXKCDFile)
        open("XKCD Transcripts Only.txt", "w")


####################################################################################

#  DELETE ALL EXISTING CONTENT IN BOTH COMICS AND XKCD Alt-Titles.TXT.


while True:
        print('\nPlease enter Y if you wish to clear your XKCD Repository. Otherwise, enter N.\n')
        requestDelete = input()
        if requestDelete.lower() == 'y':
                    print('\nARE YOU SURE? Y/N?')
                    requestDelete = input().upper()
                    if requestDelete == 'Y':
                        os.chdir(userComicFile)
                        open(userTextFile, 'w').close()
                        open(userAltFile, 'w').close()
                        open(userTranscriptFile, 'w').close()
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

##  ACQUIRE THE LATEST OWNED XKCD ISSUE FROM USER FILES
        
latestOwned = 0
latestFileRegex = re.compile(r'\[\d{1,4}\]')
digitRegex = re.compile(r'\d{1,1000}')

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

comicPage = requests.get('https://xkcd.com/info.0.json')
json_data = json.loads(comicPage.content)
latestXKCD = json_data['num']
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
                
                caption = open('_XKCD Metadata.txt', 'a')
                altFile = open('XKCD Alt Titles Only.txt', 'a')
                scriptFile = open('XKCD Transcripts Only.txt', 'a')
                
                caption.write(str([i]) + ' XKCD\'s 404 Page. Literally... nginx was here\n\n')
                altFile.write(str([i]) + ' XKCD\'s 404 Page. Literally... nginx was here\n\n')
                scriptFile.write(str([i]) + ' XKCD\'s 404 Page. Literally... nginx was here\n\n')

                caption.close()
                altFile.close()
                scriptFile.close()

                continue

    #  RESET CWD, GET JSON_DATA
    
        os.chdir(userComicFile)
        comicPage = requests.get('https://xkcd.com/' + str(i) + '/info.0.json')
        json_data = json.loads(comicPage.content)

    #  GET ALL NAMES

        name = str(json_data['safe_title'])
        name = re.sub(r'[\\/:*?"<>|]', '', name)
    
    #  ACQUIRE ALL THE IMG ALT-TITLES

        alt = str(json_data['alt'])
        alt = unidecode.unidecode(alt)

    #  GET URL
    
        url = json_data['img']
    
    #  IMPORT TO COMICS FILE
    
        img = requests.get(url, stream=True)
        with open(str([i]) + ' ' + name + '.png', 'wb') as out_file:
                shutil.copyfileobj(img.raw, out_file)
        del img

    #  GET THE DATE FROM JSON
    
        date = json_data["month"] + '/' + json_data["day"] + '/' + json_data["year"]
        transcript = unidecode.unidecode('\n'.join(json_data['transcript'].split("\n")[:-1]))

    #  IMPORT ALL METADATA TO TEXT FILE

        os.chdir(userXKCDFile)
        caption = open('_XKCD Metadata.txt', 'a')
        altFile = open('XKCD Alt Titles Only.txt', 'a')
        scriptFile = open('XKCD Transcripts Only.txt', 'a')
        
        caption.write(str([i]) + ' ' + name + '\nAlt: ' + alt + '\nDate published: ' + date + '\nTranscript:\n' + transcript + '\n\n')
        caption.close()

        altFile.write(str([i]) + ' ' + name + '\nAlt: ' + alt + '\n\n')
        altFile.close()

        scriptFile.write(str([i]) + ' ' + name + '\nTranscript:\n' + transcript + '\n\n')
        scriptFile.close

print('ALL XKCD COMICS AND ALT TITLES HAVE BEEN DOWNLOADED.')
os.system("@pause")
os.startfile(userComicFile)
os.startfile(userTextFile)
sys.exit()
