import time as t
import smbus
import sys
import RPi.GPIO as GPIO

# I2C Configuration
DEVICE_BUS = 1
DEVICE_ADDR = 0x10
bus = smbus.SMBus(DEVICE_BUS)

# Servo Configuration
SERVO_PIN = 18  # GPIO18 (Pin 12) for servo control
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
servo.start(0)  # Start with 0% duty cycle

def set_servo_angle(angle):
    """Convert angle to duty cycle and set servo position"""
    duty = angle / 18 + 2  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty)

try:
    while True:
        try:
            # I2C control loop
            for i in range(1,5):
                bus.write_byte_data(DEVICE_ADDR, i, 0xFF)
                t.sleep(1)
                bus.write_byte_data(DEVICE_ADDR, i, 0x00)
                t.sleep(1)
            
            # Servo control example
            set_servo_angle(0)    # Move to 0 degrees
            t.sleep(1)
            set_servo_angle(90)   # Move to 90 degrees
            t.sleep(1)
            set_servo_angle(180)  # Move to 180 degrees
            t.sleep(1)
            set_servo_angle(90)   # Return to center
            t.sleep(1)
            
        except KeyboardInterrupt as e:
            print("Quit the Loop")
            break
finally:
    # Cleanup
    servo.stop()
    GPIO.cleanup()
    sys.exit() 