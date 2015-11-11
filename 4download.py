#!/bin/python

import basc_py4chan
import requests
import sys
import os
import time

#setting default variables
boardLetter = "b"
#thread ID can't be a default
threadID = 0

#downloaded files are stored here
outputFolder = "."
defaultFolder = True

#all file types are rejected by default
acceptGIFs = False
acceptWebms = False
acceptPNGs = False
acceptJPGs = False

updateUntil404 = False

def downloadFile(url):
    requestModule = requests.get(url, stream=True)
    filename = url.split("/")[-1]

    with open(filename, 'wb') as outFile:
        for chunk in requestModule.iter_content(chunk_size=1024):
            if chunk:
                outFile.write(chunk)
    return filename

def acceptCheck(fileURL):
    filenameExtension = fileURL.split('.')[-1]

    if filenameExtension == "webm" and acceptWebms == True:
        return True
    elif filenameExtension == "gif" and acceptGIFs == True:
        return True
    elif filenameExtension == "jpg" and acceptJPGs == True:
        return True
    elif filenameExtension == "png" and acceptPNGs == True:
        return True

if len(sys.argv) == 1:
    print("Run ./4download.py --help for help")
else:
    if sys.argv[1] == "--help":
        print("---------------")
        print("--board [BOARD LETTER]")
        print("--thread [THREAD ID]")
        print("--all (Accepts all files)")
        print("Use the following in combinations")
        print("to accept a list of file types")
        print("--jpg (Accepts all jpgs)")
        print("--png (Accepts all pngs)")
        print("--gif (Accepts all GIFs)")
        print("--webm (Accepts all WebMs)")
        print("--output [OUTPUT FOLDER]")
        print("--update (Updates until 404)")
        print("---------------")
    else:
        cliArgs = sys.argv[1:]
        argNumber = 0

        while argNumber < len(cliArgs):
            argNumber = argNumber + 1
            if cliArgs[argNumber - 1] == "--board":
                boardLetter = cliArgs[argNumber]
            elif cliArgs[argNumber - 1] == "--thread":
                threadID = int(cliArgs[argNumber])
            elif cliArgs[argNumber - 1] == "--all":
                acceptGIFs = True
                acceptWebms = True
                acceptPNGs = True
                acceptJPGs = True
            elif cliArgs[argNumber - 1] == "--jpg":
                acceptJPGs = True
            elif cliArgs[argNumber - 1] == "--png":
                acceptPNGs = True
            elif cliArgs[argNumber - 1] == "--gif":
                acceptGIFs = True
            elif cliArgs[argNumber - 1] == "--webm":
                acceptWebms = True
            elif cliArgs[argNumber - 1] == "--output":
                outputFolder = cliArgs[argNumber]
                defaultFolder = False
            elif cliArgs[argNumber - 1] == "--update":
                updateUntil404 = True

        print("Making connection to 4chan server")

        board = basc_py4chan.Board(boardLetter)
        thread = board.get_thread(threadID)

        files = [loc for loc in thread.files()]
        print("Detected " + str(len(files)) + " file(s)")

        if defaultFolder == True:
            outputFolder = boardLetter + "_" + str(threadID)

        print("Creating folder: " + outputFolder)
        os.mkdir(outputFolder)

        print("Changing to folder: " + outputFolder)
        os.chdir(outputFolder)

        filesDownloaded = 0

        try:
            for URL in files:
                if acceptCheck(URL) == True:
                    downloadFile(URL)
                    filesDownloaded = filesDownloaded + 1
        except KeyboardInterrupt:
            print("Initial download loop stopped: KeyboardInterrupt")
            updateUntil404 = False

        if updateUntil404 == True:
            try:
                while thread.closed == False:
                    time.sleep(2)
                    if thread.closed == False:
                        thread.update()
                        files = [loc for loc in thread.files()]
                        for URL in files[filesDownloaded:]:
                            if acceptCheck(URL) == True:
                                downloadFile(URL)
                                filesDownloaded = filesDownloaded + 1
            except KeyboardInterrupt:
                print("Update loop stopped: KeyboardInterrupt")

        print("Downloaded " + str(filesDownloaded) + " files")
        print("Done")

        print("Rolling back one directory...")
        os.chdir("..")

        print("Finished. Congratulations!")
