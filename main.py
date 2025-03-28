import time
import datetime
import sys
import smbus
import RPi.GPIO as GPIO

# I2C Configuration
DEVICE_BUS = 1
DEVICE_ADDR = 0x10
bus = smbus.SMBus(DEVICE_BUS)

# Device mapping for I2C control
PUMP_AIR = 1          # Continuous air pump
SOLENOID_WATER_IN = 2 # Water inlet solenoid
PUMP_WATER_IN = 3     # Water inlet pump
PUMP_WATER_OUT = 4    # Water outlet pump

# Servo Configuration
SERVO_PIN = 18  # GPIO18 (Pin 12) for servo control

# Timing Configuration (all values in seconds)
TIMING = {
    'FEEDER_REPEAT': 1,      # Number of times to cycle the feeder pattern
    'PRIME_WATER_IN_CYCLES': 15,
    'PRIME_WATER_OUT_CYCLES': 5,
    'PUMP_ON_TIME': 0.5,
    'PUMP_OFF_TIME': 0.5,
    'CLEAN_WATER_IN_CYCLES': 9,
    'CLEAN_WATER_OUT_CYCLES': 5,
    'CLEAN_REPEAT_CYCLES': 3,
    'FINAL_CLEAN_CYCLES': 3,
    'STREAM_WATER_OUT_CYCLES': 6,
    'STREAM_WATER_IN_CYCLES': 8,
    'STREAM_REPEAT_CYCLES': 2
}

class FishFeeder:
    def __init__(self):
        self.day = None
        self.current_time = None
        self.status = None
        
        # Initialize servo
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
        self.servo.start(0)  # Start with 0% duty cycle

    def set_servo_angle(self, angle):
        """Convert angle to duty cycle and set servo position"""
        duty = angle / 18 + 2  # Convert angle to duty cycle
        self.servo.ChangeDutyCycle(duty)
        time.sleep(0.5)  # Allow time for servo to reach position

    def device_control(self, device, state):
        """Control I2C devices: 0x00 for OFF, 0xFF for ON"""
        value = 0xFF if state else 0x00
        bus.write_byte_data(DEVICE_ADDR, device, value)

    def initialize(self):
        """Initialize system and start air pump"""
        self.day, self.current_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').split()
        
        # Start air pump
        self.device_control(PUMP_AIR, True)
        # Open solenoid
        self.device_control(SOLENOID_WATER_IN, True)

    def priming(self):
        """Prime the water pumps"""
        # Prime water in
        for _ in range(TIMING['PRIME_WATER_IN_CYCLES']):
            self.device_control(PUMP_WATER_IN, True)
            time.sleep(TIMING['PUMP_ON_TIME'])
            self.device_control(PUMP_WATER_IN, False)
            time.sleep(TIMING['PUMP_OFF_TIME'])

        # Prime water out
        for _ in range(TIMING['PRIME_WATER_OUT_CYCLES']):
            self.device_control(PUMP_WATER_OUT, True)
            time.sleep(TIMING['PUMP_ON_TIME'])
            self.device_control(PUMP_WATER_OUT, False)
            time.sleep(TIMING['PUMP_OFF_TIME'])

    def prepare(self):
        """Prepare food and initial water"""
        # Dispense food
        for _ in range(TIMING['FEEDER_REPEAT']):
            self.set_servo_angle(0)
            self.set_servo_angle(180)

        # Initial water fill
        for _ in range(10):
            self.device_control(PUMP_WATER_IN, True)
            time.sleep(TIMING['PUMP_ON_TIME'])
            self.device_control(PUMP_WATER_IN, False)
            time.sleep(TIMING['PUMP_OFF_TIME'])

        self.status = "FoodPrepared"

    def stream(self):
        """Stream water and food mixture"""
        # Initial stream
        for _ in range(TIMING['STREAM_WATER_OUT_CYCLES']):
            self.device_control(PUMP_WATER_OUT, True)
            time.sleep(TIMING['PUMP_ON_TIME'])
            self.device_control(PUMP_WATER_OUT, False)
            time.sleep(TIMING['PUMP_OFF_TIME'])

        # Repeated water in/out cycles
        for _ in range(TIMING['STREAM_REPEAT_CYCLES']):
            # Water in
            for _ in range(TIMING['STREAM_WATER_IN_CYCLES']):
                self.device_control(PUMP_WATER_IN, True)
                time.sleep(TIMING['PUMP_ON_TIME'])
                self.device_control(PUMP_WATER_IN, False)
                time.sleep(TIMING['PUMP_OFF_TIME'])

            # Water out
            for _ in range(TIMING['STREAM_WATER_OUT_CYCLES']):
                self.device_control(PUMP_WATER_OUT, True)
                time.sleep(TIMING['PUMP_ON_TIME'])
                self.device_control(PUMP_WATER_OUT, False)
                time.sleep(TIMING['PUMP_OFF_TIME'])

    def clean(self):
        """Clean the system"""
        # Initial cleaning cycle
        for _ in range(TIMING['CLEAN_WATER_IN_CYCLES']):
            self.device_control(PUMP_WATER_IN, True)
            time.sleep(TIMING['PUMP_ON_TIME'])
            self.device_control(PUMP_WATER_IN, False)
            time.sleep(TIMING['PUMP_OFF_TIME'])

        for _ in range(TIMING['CLEAN_WATER_OUT_CYCLES']):
            self.device_control(PUMP_WATER_OUT, True)
            time.sleep(TIMING['PUMP_ON_TIME'])
            self.device_control(PUMP_WATER_OUT, False)
            time.sleep(TIMING['PUMP_OFF_TIME'])

        # Main cleaning cycles
        for _ in range(TIMING['CLEAN_REPEAT_CYCLES']):
            for _ in range(TIMING['CLEAN_WATER_IN_CYCLES']):
                self.device_control(PUMP_WATER_IN, True)
                time.sleep(TIMING['PUMP_ON_TIME'])
                self.device_control(PUMP_WATER_IN, False)
                time.sleep(TIMING['PUMP_OFF_TIME'])

            for _ in range(TIMING['CLEAN_WATER_OUT_CYCLES']):
                self.device_control(PUMP_WATER_OUT, True)
                time.sleep(TIMING['PUMP_ON_TIME'])
                self.device_control(PUMP_WATER_OUT, False)
                time.sleep(TIMING['PUMP_OFF_TIME'])

        # Final cleaning cycles
        for _ in range(TIMING['FINAL_CLEAN_CYCLES']):
            for _ in range(10):
                self.device_control(PUMP_WATER_IN, True)
                time.sleep(TIMING['PUMP_ON_TIME'])
                self.device_control(PUMP_WATER_IN, False)
                time.sleep(TIMING['PUMP_OFF_TIME'])

            for _ in range(6):
                self.device_control(PUMP_WATER_OUT, True)
                time.sleep(TIMING['PUMP_ON_TIME'])
                self.device_control(PUMP_WATER_OUT, False)
                time.sleep(TIMING['PUMP_OFF_TIME'])

        self.status = "Cleaned"

    def finalize(self):
        """Shut down all systems"""
        # Turn off all devices
        self.device_control(PUMP_WATER_IN, False)
        self.device_control(PUMP_WATER_OUT, False)
        self.device_control(PUMP_AIR, False)
        self.device_control(SOLENOID_WATER_IN, False)
        
        # Cleanup servo
        self.servo.stop()
        GPIO.cleanup()

        print(f"{self.day} {self.current_time} {self.status}")

def run_fishfeed():
    feeder = FishFeeder()

    try:
        # Initialize system
        feeder.initialize()
        print("initialized")

        # Prime pumps
        feeder.priming()
        print("pumps primed")

        # Prepare food
        feeder.prepare()
        print("food prepared")

        # Stream food and water
        feeder.stream()
        print("food water mix streamed")

        # Clean system
        feeder.clean()
        print("tanks cleaned")

    except KeyboardInterrupt:
        print("\nCtrl-C pressed. Program exiting...")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        # Finalize and cleanup
        feeder.finalize()
        print("finalized")
        sys.exit()

if __name__ == '__main__':
    run_fishfeed() 