from pywatlow import PM3

watlow = PM3(port='COM3')

watlow.readParam('4001')
watlow.readParam('7001')
watlow.setTemp(100)

#second_watlow = PM3(watlow.serial, address=2)
second_watlow = PM3(address=2)
second_watlow.serial = watlow.serial

second_watlow.readParam('4001')
second_watlow.readParam('7001')
second_watlow.setTemp(100)

print(second_watlow.serial.port)

watlow.close()
