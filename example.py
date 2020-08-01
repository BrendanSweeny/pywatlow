from pywatlow.watlow import Watlow
watlow = Watlow(port='COM5', address=1)

print(watlow.read(8003))
print(watlow.write(64, 8003, int))

# pywatlow will call read() to determine message structure if no val_type is provided
print(watlow.write(71, 8003))

print(watlow.write(71, 8003, float))
