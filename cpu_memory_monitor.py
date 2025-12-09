#!/usr/bin/env python3
"""
CPU/Memory RGB Monitor - LED colors reflect system load
Red = CPU usage, Green = Free memory, Blue = Temperature
"""
import RPi.GPIO as GPIO
import time
import psutil
import sys

# GPIO pins for RGB LED
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

def setup_gpio():
    """Initialize GPIO pins safely"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    
    red_pwm = GPIO.PWM(RED_PIN, 1000)
    green_pwm = GPIO.PWM(GREEN_PIN, 1000)
    blue_pwm = GPIO.PWM(BLUE_PIN, 1000)
    
    red_pwm.start(0)
    green_pwm.start(0)
    blue_pwm.start(0)
    
    return red_pwm, green_pwm, blue_pwm

def cleanup_gpio(red_pwm, green_pwm, blue_pwm):
    """Clean shutdown of GPIO"""
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()

def get_cpu_temp():
    """Get CPU temperature if available"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = float(f.read().strip()) / 1000.0
            return temp
    except:
        return 50.0  # Default if cant read

def cpu_memory_monitor():
    """Monitor system stats and reflect in RGB LED"""
    print("📊 CPU/Memory Monitor - Press Ctrl+C to exit")
    print("Red = CPU usage | Green = Available memory | Blue = Temperature")
    
    try:
        red_pwm, green_pwm, blue_pwm = setup_gpio()
        
        while True:
            # Get system stats
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_available = 100 - memory.percent
            cpu_temp = get_cpu_temp()
            
            # Convert stats to LED intensity (0-100%)
            red_intensity = min(cpu_percent, 100)
            green_intensity = min(memory_available, 100)
            
            # Temperature mapping (30-80C -> 0-100%)
            temp_normalized = max(0, min(100, (cpu_temp - 30) * 2))
            blue_intensity = temp_normalized
            
            # Update LEDs
            red_pwm.ChangeDutyCycle(red_intensity)
            green_pwm.ChangeDutyCycle(green_intensity)
            blue_pwm.ChangeDutyCycle(blue_intensity)
            
            # Print current stats
            print(f"\rCPU: {cpu_percent:5.1f}% | Memory: {memory_available:5.1f}% free | Temp: {cpu_temp:4.1f}°C", end="", flush=True)
            
            time.sleep(1)  # Update every second
            
    except KeyboardInterrupt:
        print("\n📊 Monitoring stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        cleanup_gpio(red_pwm, green_pwm, blue_pwm)
        print("✅ GPIO cleaned up safely")

if __name__ == "__main__":
    cpu_memory_monitor()
