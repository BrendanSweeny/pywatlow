from pywatlow.watlow import Watlow
watlow = Watlow(port='COM5', address=1)
print(watlow.read())
print(watlow.readSetpoint())
print(watlow.write(55))
