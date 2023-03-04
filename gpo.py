import sys
import guitarpro
import os
import shutil
import math

filesToTest = []
errorFiles = []
fileCount = 0
totalFiles = 0
tuningCounts = {}
directionInput = os.path.join(os.getcwd())
directionOutput = directionInput
progress = ""


notes = {
    "C": [0,12,24,36,48,60],
    "Db":[1,13,25,37,49,61],
    "D":[2,14,26,38,50,62],
    "Eb":[3,15,27,39,51,63],
    "E": [4,16,28,40,52,64],
    "F":[5,17,29,41,53,65],
    "Gb":[6,18,30,42,54,66],
    "G":[7,19,31,43,55,67],
    "Ab":[8,20,32,44,56,68],
    "A":[9,21,33,45,57,69],
    "Bb":[10,22,34,46,58,70],
    "B":[11,23,35,47,59,71]
}

def checkTuning(firstString,secondString):
    if(firstString in notes["E"] and secondString in notes["A"]):
        return "standard E"
    elif(firstString in notes["D"]):
        if(secondString in notes["G"]):
            return "standard D"
        elif(secondString in notes["A"]):
            return "drop D"
        else:
            return "unknown"
    elif(firstString in notes["Eb"] and secondString in notes["Ab"]):
        return "standard Eb"
    elif(firstString in notes["C"]):
        if(secondString in notes["F"]):
            return "standard C"
        elif(secondString in notes["G"]):
            return "drop C"
        else:
            return "unknown"
    elif(firstString in notes["B"]):
        if(secondString in notes["E"]):
            return "standard B"
        elif(secondString in notes["Gb"]):
            return "drop B"
        else:
            return "unknown"
    elif(firstString in notes["Db"] and secondString in notes["Ab"]):
        return "drop Db"
    else:
        return "unknown"



def checkSong(gpFile, action):

    global filesToTest
    global errorFiles
    global fileCount
    global totalFiles
    global tuningCounts
    global directionInput
    global directionOutput
    
    try:
        song = guitarpro.parse(directionInput +"/"+ gpFile)
        possibleTunings = {} 

        for track in song.tracks:
            if (track.isPercussionTrack == False):

                tuning = checkTuning(track.strings[len(track.strings) -1].value,track.strings[len(track.strings) -2].value)
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
    except:
        errorFiles.append(gpFile)

def processFiles(action):

    global filesToTest
    global errorFiles
    global fileCount
    global totalFiles
    global tuningCounts
    global directionInput
    global directionOutput
    global progress

    tuningCounts = {}
    files = os.listdir(os.path.abspath(directionInput))

    for file in files:
        totalFiles += 1
        if file.endswith(('.gp5', '.gp4', '.gp3')):
            filesToTest.append(file)
        else:
            errorFiles.append(file)

    print("analysing / organizing files...")
    for gpFile in filesToTest:
        fileCount = fileCount + 1
        hashtags = math.floor((math.floor((fileCount / len(filesToTest)) * 100)) / 5)
        progress = "[" + str("#" * hashtags) + ("_" * (20 - hashtags)) + "]" + " " + str(math.floor((fileCount / len(filesToTest)) * 100)) + "%"
        print(progress, end="\r")
        checkSong(gpFile, action)

    errorFilesString = ""
    for file in errorFiles:
        errorFilesString = errorFilesString + "    " + file + "\n"

    stringToWrite = ""
    for tuning in tuningCounts:
        stringToWrite += tuning + " " + "found:     " + " " + str(tuningCounts[tuning]) + "\n"

    if(action == "analyze"):
        print("\n" + stringToWrite)

    if(outputFile == True):
        if not os.path.isdir(directionOutput):
            os.makedirs(directionOutput)
        outputLog = directionOutput + "/" + "Analyzed files.txt"

        f = open(outputLog, "w")
        f.write(stringToWrite)
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
    outputFile = False
    processFiles("analyze")



