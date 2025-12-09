#!/usr/bin/env python3
"""
Low Voltage Warning RGB Effect
Monitors Pi voltage and shows warning colors
"""
import RPi.GPIO as GPIO
import time
import subprocess
import re

# GPIO pins
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([RED_PIN, GREEN_PIN, BLUE_PIN], GPIO.OUT)
    
    # Create PWM objects for smooth color control
    red_pwm = GPIO.PWM(RED_PIN, 1000)
    green_pwm = GPIO.PWM(GREEN_PIN, 1000)
    blue_pwm = GPIO.PWM(BLUE_PIN, 1000)
    
    red_pwm.start(0)
    green_pwm.start(0)
    blue_pwm.start(0)
    
    return red_pwm, green_pwm, blue_pwm

def get_voltage():
    """Get Pi voltage using vcgencmd"""
    try:
        result = subprocess.run(["vcgencmd", "measure_volts", "core"], 
                              capture_output=True, text=True)
        voltage_str = result.stdout.strip()
        # Extract voltage number (format: "volt=1.2000V")
        match = re.search(r"(\d+\.\d+)V", voltage_str)
        if match:
            return float(match.group(1))
        return 1.2  # Default safe value
    except:
        return 1.2  # Default if command fails

def set_color(red_pwm, green_pwm, blue_pwm, red, green, blue):
    """Set RGB color (0-100 for each channel)"""
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

def voltage_warning_effect():
    """Main voltage monitoring effect"""
    red_pwm, green_pwm, blue_pwm = setup_gpio()
    
    try:
        print("🔋 Low Voltage Warning Active")
        print("💡 RGB will show voltage status:")
        print("   🟢 Green = Good voltage (>1.15V)")
        print("   🟡 Yellow = Low voltage (1.10-1.15V)")  
        print("   🔴 Red = Critical voltage (<1.10V)")
        print("   💙 Blue pulse = Checking voltage...")
        print("\nPress Ctrl+C to exit\n")
        
        while True:
            # Blue pulse while checking
            set_color(red_pwm, green_pwm, blue_pwm, 0, 0, 50)
            time.sleep(0.1)
            set_color(red_pwm, green_pwm, blue_pwm, 0, 0, 0)
            time.sleep(0.1)
            
            # Get current voltage
            voltage = get_voltage()
            print(f"📊 Voltage: {voltage:.3f}V", end=" - ")
            
            if voltage > 1.15:
                # Good voltage - solid green
                print("🟢 GOOD")
                set_color(red_pwm, green_pwm, blue_pwm, 0, 100, 0)
                time.sleep(2.0)
                
            elif voltage > 1.10:
                # Low voltage - yellow warning
                print("🟡 LOW WARNING")
                for _ in range(6):  # Flash yellow
                    set_color(red_pwm, green_pwm, blue_pwm, 100, 100, 0)
                    time.sleep(0.3)
                    set_color(red_pwm, green_pwm, blue_pwm, 0, 0, 0)
                    time.sleep(0.3)
                    
            else:
                # Critical voltage - red alarm
                print("🔴 CRITICAL!")
                for _ in range(10):  # Fast red flash
                    set_color(red_pwm, green_pwm, blue_pwm, 100, 0, 0)
                    time.sleep(0.15)
                    set_color(red_pwm, green_pwm, blue_pwm, 0, 0, 0)
                    time.sleep(0.15)
            
            time.sleep(1)  # Check every few seconds
            
    except KeyboardInterrupt:
        print("\n🔋 Voltage monitoring stopped")
    finally:
        # Clean shutdown
        set_color(red_pwm, green_pwm, blue_pwm, 0, 0, 0)
        red_pwm.stop()
        green_pwm.stop()
        blue_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    voltage_warning_effect()
