#!/usr/bin/python3
""" Test the Storage """

if __name__ == "__main__":
    import models
    marker = models.classes["Marker"]()
    print(marker.id)
    marker.save()
    print(models.storage.all())
    marker.delete()
    print(models.storage.all())
