import serial


try:
    ser = serial.Serial("COM3")
    print("hi")
    while ser.read():
        print("serial open")
    print("serial closed")
    ser.close()
except serial.serialutil.SerialException:
    print('exception')
