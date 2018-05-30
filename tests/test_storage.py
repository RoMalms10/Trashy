#!/usr/bin/python3
""" Test the Storage """

if __name__ == "__main__":
    import sys
    print(sys.path)
    import models
    marker = models.classes["Marker"]
    print(marker.id)
