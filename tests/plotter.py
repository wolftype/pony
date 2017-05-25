import serial

ser = serial.Serial('/dev/tty.usbserial')

ser.baudrate=9600
ser.xonxoff=1
ser.timeout=1
ser.parity=serial.PARITY_ODD

print ser

_esc = chr(27)
_id = _esc+".A"
_on = _esc+".Y"
_in = _esc+".IN"

ser.flushInput()
ser.flushOutput()
ser.write (b'\A')
ser.readline()
ser.close()


