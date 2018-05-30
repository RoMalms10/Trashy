#!/usr/bin/python3
""" Test the Storage """

if __name__ == "__main__":
    import models
    import csv
    marker = models.classes["Marker"]()
    print("Marker: " + marker.id)
    user = models.classes["User"]()
    print("User: " + user.id)
    user.save()
    marker.user_id = user.id
    marker.save()
    print(models.storage.all())
    marker.delete()
    user.delete()
    print(models.storage.all())
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
            break
    print(new_dict)
    marker = models.classes["Marker"](**new_dict)
    marker.save()
    print(marker)
    marker.delete()
    print(models.storage.all())
