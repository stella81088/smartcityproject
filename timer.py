import time
import board
from busio import I2C
import adafruit_bme680
import adafruit_tsl2591
from gpiozero import MotionSensor

def time_convert(sec): #stopwatch calculation
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# sensor for TSL
sensor = adafruit_tsl2591.TSL2591(i2c)

#sensor for PIR 
pir = MotionSensor(4)

while True:
    try:
        #PIR motion sensor
        print ("")
        print ("MOTION DETECTION")
        pir.wait_for_motion()
        start_time = time.time() #getting start time
        print("You moved")
        pir.wait_for_no_motion()
        end_time = time.time() #getting end time
        print("waiting for motion")
        
        #time calculator for PIR motion sensor
        time_lapsed = end_time - start_time
        time_convert(time_lapsed)

        #BME680 sensor
        print ("BME680 sensor readings")
        print("\nTemperature: %0.1f C" % bme680.temperature)
        print("Gas: %d ohm" % bme680.gas)
        print("Humidity: %0.1f %%" % bme680.humidity)
        print("Pressure: %0.3f hPa" % bme680.pressure)
        print("Altitude = %0.2f meters" % bme680.altitude)

        #TSL sensor
        print ("TSL sensor readings")
        lux = sensor.lux
        print ("")
        print ("TSL sensor readings")
        print('Total light: {0}lux'.format(lux))
        # You can also read the raw infrared and visible light levels.
        # These are unsigned, the higher the number the more light of that type.
        # There are no units like lux.
        # Infrared levels range from 0-65535 (16-bit)
        infrared = sensor.infrared
        print('Infrared light: {0}'.format(infrared))
        # Visible-only levels range from 0-2147483647 (32-bit)
        visible = sensor.visible
        print('Visible light: {0}'.format(visible))
        # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
        full_spectrum = sensor.full_spectrum
        print('Full spectrum (IR + visible) light: {0}'.format(full_spectrum))

        time.sleep(3)
    except:
        continue
