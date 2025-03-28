# Fish Feeder

This project controls a fish feeder device via I2C communication and servo control on a Raspberry Pi 4.

## Prerequisites

- Raspberry Pi 4
- Python 3.x
- I2C enabled on Raspberry Pi
- Servo motor (compatible with 5V power)
- I2C relay board with 4 channels

## Setup

1. Enable I2C on your Raspberry Pi:
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > I2C > Enable
   ```

2. Add your user to the gpio group to allow GPIO access without sudo:
   ```bash
   sudo usermod -a -G gpio $USER
   # You'll need to log out and back in for this to take effect
   ```

3. Install required Python packages:
   ```bash
   pip install smbus-cffi RPi.GPIO
   ```

4. Clone this repository:
   ```bash
   git clone <your-repository-url>
   cd FishFeeder-Tester
   ```

5. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

6. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Usage

Run the main script:
```bash
python main.py
```

The script will execute the following sequence:
1. Initialize the system and start the air pump
2. Prime the water pumps (inlet and outlet)
3. Prepare food by dispensing through the servo mechanism
4. Stream the food and water mixture
5. Clean the system with multiple water cycles

To stop the program, press Ctrl+C.

## Hardware Setup

### I2C Device
- Connect the I2C device to the Raspberry Pi's I2C pins:
  - SDA: GPIO 2 (Pin 3)
  - SCL: GPIO 3 (Pin 5)
- Device address: 0x10
- I2C bus: 1
- Channel mapping:
  - Channel 1: Air pump (continuous operation)
  - Channel 2: Water inlet solenoid
  - Channel 3: Water inlet pump
  - Channel 4: Water outlet pump

### Servo Motor
- Connect the servo motor to the following pins:
  - Signal wire: GPIO 18 (Pin 12)
  - Power wire: 5V
  - Ground wire: Any GND pin
- The servo will be controlled using PWM at 50Hz frequency
- The servo can be positioned at any angle between 0° and 180°

## Configuration

The system's timing parameters can be adjusted in the `TIMING` dictionary in `main.py`:

```python
TIMING = {
    'FEEDER_REPEAT': 1,      # Number of times to cycle the feeder pattern
    'PRIME_WATER_IN_CYCLES': 15,
    'PRIME_WATER_OUT_CYCLES': 5,
    'PUMP_ON_TIME': 0.5,     # Time each pump stays on
    'PUMP_OFF_TIME': 0.5,    # Time between pump activations
    'CLEAN_WATER_IN_CYCLES': 9,
    'CLEAN_WATER_OUT_CYCLES': 5,
    'CLEAN_REPEAT_CYCLES': 3,
    'FINAL_CLEAN_CYCLES': 3,
    'STREAM_WATER_OUT_CYCLES': 6,
    'STREAM_WATER_IN_CYCLES': 8,
    'STREAM_REPEAT_CYCLES': 2
}
```

All timing values are in seconds.

## Pump Assembly

This project is based on the [ZAF, the first open source fully automated feeder for aquatic facilities](https://elifesciences.org/articles/74234) which relied on the [ZAF GitHub Repo](https://arc.net/l/quote/wmihusja).

**Why change it?** The original ZAF used a lot of small extruded aluminum, zip ties/epoxy, and a bloated elecrtonic BOM. In an effort to fit this in our fish facility, the Neurotech Hub developed [parts in Fusion 360](https://a360.co/4j6lC9R) for a more ideal and bespoke installation.

For our prototype, we are utilizing pumps for air, water in, and water out. The solenoid is also installed for your use. I have procured a float sensor should we want to detect overflowing water.

### Managing with Github

This project lives in the `FishFeeder` folder. Open terminal on the Raspberry Pi:

```bash
cd FishFeeder
python main.py
```

To open that folder:

```bash
cd FishFeeder
open .
```

To pull changes from GitHub:

```bash
cd FishFeeder
git pull origin main
```

### Feeding with Servo

The Raspberry Pi can natively drive a servo motor. The [Food Drum](https://a360.co/3DWRvmp) and [Container Fixture](https://a360.co/4hTFQTl) were designed in Fusion 360. The drum press-fits onto the servo motor and has two methods of controlling food quantity:

1. Sliding acrylic door.
2. Modifying `FEEDER_REPEAT` in the code.