#!/usr/bin/python3
"""
"""
import models
import csv

if __name__ == "__main__":

    with open('trash_cans.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar="|")
        for row in data:
            new_dict = {}
            new_dict['name'] = row[1]
            lat = row[2].strip("\"")
            lat = lat.strip("(")
            new_dict['latitude'] = float(lat)
            lng = row[3].strip("\"")
            lng = lng.strip(")")
            lng = lng.strip(" ")
            new_dict['longitude'] = float(lng)
            marker = models.classes["Marker"](**new_dict)
            marker.save()
    print(len(models.storage.all()))
