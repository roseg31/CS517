# Scheduler Using SAT Solver
# By Rosalinda Garcia

import time
from pysmt.shortcuts import Symbol, And, Or, Not, get_model

workshopDuration = int(input("How long should the workshop be? (give an integer number of hours)\n"))
workshopMinParticipation = int(input(
    "What's the minimum number of attendees you want there at any give time? (give an integer number of attendees)\n"))
inputFileName = input("What's the file name for the input?\n")


def scheduler(t, k):
    # Rules:
    # 1: The selected time is t hours long
    # each hour has at least k faculty
    # Each faculty attends at least t-1 hours

    # Define some variables we'll be using
    startTime = time.time()
    numFaculty = len(inputArr)
    hourSymbols = [Symbol("h1"), Symbol("h2"), Symbol("h3"), Symbol("h4"), Symbol("h5"), Symbol("h6"), Symbol("h7"),
                   Symbol("h8")]
    numOptions = 8 - t + 1

    # The selected time is t hours long
    if t > 8:
        print("Days are 8 hours, please reduce workshop length")
        return

    hourOptions = []
    for x in range(numOptions):
        tempHours = []
        for y in range(t):
            tempHours.append(hourSymbols[y + x])
        tempHourFormula = And(tempHours)
        hourOptions.append(tempHourFormula)

    rule1Hours = Or(hourOptions)

    # Rule 2: each hour has at least k faculty (here implemented as "don't include hours that have less than k faculty")
    hoursMet = []
    for h in range(8):
        sumF = 0
        for x in range(numFaculty):
            sumF += inputArr[x][h]
        if sumF < k:
            hoursMet.append(Not(hourSymbols[h]))
    rule2MinFaculty = And(hoursMet)

    # rule 3: all faculty have to attend at least k-1 hours
    completeHoursNotOk = []
    rule3MinAttendance = ""
    for f in range(numFaculty):  # for each faculty member
        if 0 in inputArr[f]:  # if they have any unavailable times
            hoursNotOk = []
            for x in range(numOptions):  # go through each possible time slot
                tempAvailability = []
                tempHours = []
                for y in range(t):
                    tempAvailability.append(inputArr[f][y + x])  # record the number of hours attended for the timeslot
                    tempHours.append(Not(hourSymbols[y + x]))  # and record the hours in the time slot
                if sum(tempAvailability) < t - 1:  # if there are less than t-1 hours in the time slot
                    tempHourFormula = Or(tempHours)
                    hoursNotOk.append(tempHourFormula)  # add these hours to the no list

            if len(hoursNotOk):
                facultyHoursNotOk = And(hoursNotOk)  # make sure we can't choose any of these "no ok" hour slots
                completeHoursNotOk.append(facultyHoursNotOk)

    rule3MinAttendance = And(completeHoursNotOk)
    print(rule3MinAttendance)

    finalFormula = And(rule1Hours, rule2MinFaculty, rule3MinAttendance)
    model = get_model(finalFormula)
    if model:
        print(model)
    else:
        print("No solution\n")

    endTime = time.time()
    print("Calculation took " + str(endTime-startTime) + " seconds.")

def readInputFile(filename):
    fileObj = open(filename, "r")
    arrStrings = fileObj.readlines()
    fileObj.close()
    arrInts = []
    for a in arrStrings:
        lineArr = a.split(" ")
        lineIntArr = [int(i) for i in lineArr]
        arrInts.append(lineIntArr)

    return arrInts


inputArr = readInputFile(inputFileName)
scheduler(workshopDuration, workshopMinParticipation)
