from pywatlow.watlow import Watlow
watlow = Watlow(port='COM5', address=1)

print(watlow.readParam(8003, int))
print(watlow.writeParam(8003, 64, int))
print(watlow.writeParam(8003, 71, int))

# Here the incorrect data type is given:
print(watlow.writeParam(8003, 71, float))
