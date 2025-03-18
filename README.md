# Fish Feeder Tester

This project controls a fish feeder device via I2C communication and servo control on a Raspberry Pi 4.

## Prerequisites

- Raspberry Pi 4
- Python 3.x
- I2C enabled on Raspberry Pi
- Servo motor (compatible with 5V power)

## Setup

1. Enable I2C on your Raspberry Pi:
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > I2C > Enable
   ```

2. Clone this repository:
   ```bash
   git clone <your-repository-url>
   cd FishFeeder-Tester
   ```

3. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Cycle through the feeder ports via I2C, activating each one for 1 second with a 1-second delay between activations
2. Control the servo motor through a sequence of positions (0° → 90° → 180° → 90°)

To stop the program, press Ctrl+C.

## Hardware Setup

### I2C Device
- Connect the I2C device to the Raspberry Pi's I2C pins:
  - SDA: GPIO 2 (Pin 3)
  - SCL: GPIO 3 (Pin 5)
- Device address: 0x10
- I2C bus: 1

### Servo Motor
- Connect the servo motor to the following pins:
  - Signal wire: GPIO 18 (Pin 12)
  - Power wire: 5V
  - Ground wire: Any GND pin
- The servo will be controlled using PWM at 50Hz frequency
- The servo can be positioned at any angle between 0° and 180° 