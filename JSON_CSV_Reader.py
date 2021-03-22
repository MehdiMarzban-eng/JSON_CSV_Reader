import json
import csv
import math

jsonFile = open("input.json", )

jsonData = json.loads(jsonFile.read())

totalData = {}



class sensorID:
    def __init__(self): #default constructor for the id class
        self.csvID = -1
        self.JsonID = -1

    def set_csv(self, csv):
        self.csvID = csv

    def set_json(self, json):
        self.JsonID = json

    def toString(self):
        string = str(self.csvID) + ":" + str(self.JsonID)
        return string


class latLong:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def toString(self, id):
        idString = id.toString()
        return idString

    def distance(self, args):  # check to see if the difference of both is 100 or less using the haversine formula
        earthRadius = 6371000
        subLat = math.radians(int(self.lat - float(args.lat)))
        subLong = math.radians(int(self.long - float(args.long)))
        # using the haversine formula with the math library
        stepOne = math.sin(subLat / 2) * math.sin(subLat / 2) + math.cos(
            math.radians(self.lat) * math.cos(math.radians(float(args.lat)))) * math.sin(subLong / 2) * math.sin(
            subLong / 2)

        stepTwo = 2 * math.atan2(math.sqrt(abs(stepOne)), math.sqrt(abs(1 - stepOne)))

        stepThree = earthRadius * stepTwo  # should be equal to the distance of the two points in metres

        if (subLat == 0 and subLong == 0): #checks to see if the lat long values are equal
            return 2
        elif (stepThree < 100): #checks to see if the coordiantes are within the 100 m using the haversine equation
            return 1
        else:
            return 0


with open("input.csv") as csvFile: # here we read through the csv file first and fill up the python dictionary with all the initial values
    csvReader = csv.reader(csvFile, delimiter=',')
    for i in csvReader:
        if len(i)==0:
            continue
        if i[0] != "Id":  # makes sure we skip the first row with the titles, here we're filling the dictionary
            current = latLong(float(i[1]), float(i[2]))
            id = sensorID()
            id.set_csv(i[0])
            totalData[id] = current


for i in jsonData: #in this for loop we read through the json file next, and utilizing an nested for loop we compare all of the csv id's with the current json ID
    id=int(i["Id"])
    latitude = float(i["Latitude"])
    longitude = float(i["Longitude"])
    current = latLong(latitude, longitude)
    hey = 0
    exists = 0
    Threshold = 0
    same=0

    for j in totalData:  # need to compare the current latLong to the total data dictionary
        Threshold = current.distance(totalData[j])
        if Threshold == 2: #when they are the exact same latlong values
            same=1
            break
        elif Threshold == 1: #when the values are within 100m
            continue
    if exists == 1:
        j.set_json(id)
    elif same==1:
        j.set_json(id)
    else:
        new = sensorID()
        new.set_json(id)
        totalData[new] = current

f=open("output.txt","w")
for i in totalData: # in this for loop we write to the ouput.txt file and also output the data
    outputLine=totalData[i].toString(i)
    print(outputLine)
    f.write(outputLine+"\n")

