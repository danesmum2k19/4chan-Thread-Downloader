#!/bin/python

import basc_py4chan
import wget
import sys
import os

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

        for URL in files:
            if URL[-3:] == "jpg" and acceptJPGs == True:
                wget.download(URL)
                filesDownloaded = filesDownloaded + 1
            elif URL[-3:] == "png" and acceptPNGs == True:
                wget.download(URL)
                filesDownloaded = filesDownloaded + 1
            elif URL[:-3] == "gif" and acceptGIFs == True:
                wget.download(URL)
                filesDownloaded = filesDownloaded + 1
            elif URL[-4:] == "webm" and acceptWebms == True:
                wget.download(URL)
                filesDownloaded = filesDownloaded + 1
            #making newline to clean up wget
            print()

        print("Downloaded " + str(filesDownloaded) + " files")
        print("Done")

        print("Rolling back one directory...")
        os.chdir("..")

        print("Finished. Congratulations!")
