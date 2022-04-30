import sys
import guitarpro
import os
import shutil
import math

def checkTuning(firstString,secondString):

    if ("E" in firstString) and ("A" in secondString):
        return "standard E"

    elif ("D#" in firstString) and ("G#" in secondString):
        return "standard Eb"

    elif ("D" in firstString) and ("G" in secondString):
        return "standard D"

    elif ("C" in firstString) and ("F" in secondString):
        return "standard C"

    elif ("B" in firstString) and ("E" in secondString):
        return "standard B"

    elif ("D" in firstString) and ("A" in secondString):
        return "drop D"

    elif ("C#" in firstString) and ("G#" in secondString):
        return "drop Db"
    
    elif ("C" in firstString) and ("G" in secondString):
        return "drop C"
    
    elif ("B" in firstString) and ("F#" in secondString):
        return "drop B"
    
    else:
        return "unknown"

def processFiles(action):

    directionInput = os.path.join(os.getcwd())
    directionOutput = directionInput

    filesToTest = []
    errorFiles = []
    fileCount = 0
    totalFiles = 0
    files = os.listdir(os.path.abspath(directionInput))

    for file in files:
        totalFiles += 1
        if file.endswith(('.gp5', '.gp4', '.gp3')):
            filesToTest.append(file)
        else:
            errorFiles.append(file)

    tuningCounts = {}
    for gpFile in filesToTest:
        try:
            song = guitarpro.parse(directionInput +"/"+ gpFile)
        except:
            errorFiles.append(gpFile)

        tracks = (track for track in song.tracks)
        possibleTunings = {} 

        for track in tracks:
            if (track.isPercussionTrack == False):

                strings = track.strings

                firstString = str(strings[len(strings) -1])
                secondString = str(strings[len(strings) -2])

                tuning = checkTuning(firstString,secondString)
                if tuning in possibleTunings:
                    possibleTunings[tuning] += 1
                else:
                    possibleTunings[tuning] = 1         
            
        finalTuning = max(possibleTunings, key=possibleTunings.get)

        for possibleTuning in possibleTunings:
            possibleTunings[possibleTuning] = 0

        if tuning in tuningCounts:
            tuningCounts[tuning] += 1
        else:
            tuningCounts[tuning] = 1
        
        if(action == "copy"):

            pathToCopy = os.path.join(directionOutput, tuning)

            if not os.path.isdir(pathToCopy):
                os.makedirs(pathToCopy)
            
            shutil.copy(directionInput +"/"+ gpFile, pathToCopy) 

        elif(action == "move"):
            pathToMove = os.path.join(directionOutput, tuning)

            if not os.path.isdir(pathToMove):
                os.makedirs(pathToMove)

            shutil.move(directionInput +"/"+ gpFile, pathToMove)
        
        fileCount = fileCount + 1
        progress = str(math.floor((fileCount / len(filesToTest))*100)) + "%"
        print(progress, end="\r")

    print("Done!")
    effectiveness = str(int((fileCount / totalFiles) * 100)) + "%"

    errorFilesString = ""
    for file in errorFiles:
        errorFilesString = errorFilesString + "    " + file + "\n"

    stringToWrite = ""
    for tuning in tuningCounts:
        stringToWrite += tuning + " " + "found:     " + " " + str(tuningCounts[tuning]) + "\n"

    if(action == "analyze"):
        print("\n" + stringToWrite + "\n" + "\n" +
                "Effectiveness:      " + effectiveness + "\n" + "\n" +
                "Couldn't analyze these:" + "\n" + "\n" +
                errorFilesString )

    if(outputFile == True):
        if not os.path.isdir(directionOutput):
            os.makedirs(directionOutput)
        outputLog = directionOutput + "/" + "Analyzed files.txt"

        f = open(outputLog, "w")
        f.write(stringToWrite + "\n" + "\n" +
                "Effectiveness:      " + effectiveness + "\n" + "\n" +
                "Couldn't analyze these:" + "\n" + "\n" +
                errorFilesString )
        f.close()
      
if(len(sys.argv) >= 2 and len(sys.argv) <= 3):

    if(sys.argv[1] != "-C" and sys.argv[1] != "-M" and sys.argv[1] != "-A" and sys.argv[1] != "-H"):
        print("Invalid arguments. First argument should be: -C to copy the files, -M to move the files or -A to analyze the files")

    elif(sys.argv[1] == "-H"):
        print("\nUsage: python gpo.py [action] [outputFile]\n\n" +
                "       [action]      use -C to copy files, -M to move the files or -A to analyze them\n" +
                "       [outputFile]  use -F to write a file with the results (optional)\n\n" +
                "Example: python gpo.py -C -F\n") 
    
    else:
        if(len(sys.argv)== 3 and sys.argv[2] == "-F"):
            outputFile = True
        else:
            outputFile = False

        if(sys.argv[1] == "-C"):
            processFiles("copy")
        elif(sys.argv[1] == "-M"):
            processFiles("move")
        elif(sys.argv[1] == "-A"):
            processFiles("analyze")   
else:
    print("Error. Use the -H argument to see how to use it")



