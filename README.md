# PiRGB LED Controller 🌈

Simple RGB LED controller for Raspberry Pi with visual effects and system monitoring.

## Features ✨

- **4 LED Effects:**
  - 🌈 Gentle Color Shift - Smooth rainbow transitions
  - 📊 CPU/Memory Monitor - Visual system performance
  - ⚠️ Low Voltage Warning - Red flash when power is low
  - 🔄 All effects can run in background

- **Easy Menu System** - Simple `./menu` interface
- **Background Services** - Effects survive terminal closure
- **Safe & Simple** - No OS modifications, just GPIO control

## Hardware Setup 🔌

Connect RGB LED to Raspberry Pi GPIO pins:

```
RGB LED    →  Raspberry Pi
Red   pin  →  GPIO 17 (Pin 11)
Green pin  →  GPIO 27 (Pin 13) 
Blue  pin  →  GPIO 22 (Pin 15)
Ground     →  Any GND pin
```

**Important:** Use 220Ω resistors on each color line!  If you don't have anything  else, or do not want them as bright.
You can use   100-220Ω on the green  and blue 
Or 150-220Ω on the Red

## Installation 🚀

```bash
# Clone or download this project
git clone [your-repo-url]
cd PiRGB

# Run installation
./install.sh

# Start the program
cd RGB
./menu
```

## Usage 📱

1. Run the menu: `cd RGB && ./menu`
2. Choose an effect (1-3)
3. Choose normal or background mode
4. Press Ctrl+C to stop effects
5. Use option 5 to stop all background services

## Effects Details 🎨

### 1. Gentle Color Shift
- Smooth rainbow color cycling
- Perfect for ambient lighting
- Low CPU usage

### 2. CPU/Memory Monitor  
- Green = Low usage
- Yellow = Medium usage
- Red = High usage
- Updates every second

### 3. Low Voltage Warning
- Monitors Pi power supply
- Red flashing when voltage drops
- Helps prevent corruption

## Background Mode 🔄

Any effect can run in background:
- Survives terminal closure
- Continues after logout
- Starts automatically on boot (if enabled)
- Stop with menu option 5

## Troubleshooting 🔧

**LED not working:**
- Check wiring connections
- Verify resistors are installed
- Run `sudo apt install python3-rpi.gpio`
- Make sure user is in gpio group

**Permission errors:**
- Run: `sudo usermod -a -G gpio $USER`
- Log out and back in
- Or run with `sudo`

**Effects not stopping:**
- Use menu option 5 to kill all
- Or run: `pkill -f "rgb_"`

## Project Structure 📁

```
PiRGB/
├── install.sh          # Installation script
├── README.md           # This file
└── RGB/
    ├── menu            # Main menu script
    ├── gentle_color_shift.py
    ├── cpu_memory_monitor.py
    └── low_voltage_warning.py
```

## Contributing 🤝

This is a simple educational project. Feel free to:
- Add new LED effects
- Improve the menu system  
- Add more monitoring features
- Submit issues and improvements

## License 📄

Open source - use freely for educational and personal projects.

---

**Enjoy your RGB LED controller! 🌈✨**
