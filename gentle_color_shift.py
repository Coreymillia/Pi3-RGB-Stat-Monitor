#!/usr/bin/env python3
"""
Gentle RGB Color Shift - Smooth color transitions
Safe GPIO control with proper cleanup
"""
import RPi.GPIO as GPIO
import time
import math
import sys

# GPIO pins for RGB LED
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

def setup_gpio():
    """Initialize GPIO pins safely"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Set up PWM pins
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    
    # Create PWM instances
    red_pwm = GPIO.PWM(RED_PIN, 1000)    # 1kHz frequency
    green_pwm = GPIO.PWM(GREEN_PIN, 1000)
    blue_pwm = GPIO.PWM(BLUE_PIN, 1000)
    
    # Start PWM with 0% duty cycle
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

def gentle_color_shift():
    """Smooth color transitions through rainbow spectrum"""
    print("🌈 Gentle Color Shift - Press Ctrl+C to exit")
    print("Cycling through rainbow colors smoothly...")
    
    try:
        red_pwm, green_pwm, blue_pwm = setup_gpio()
        
        hue = 0
        while True:
            # Convert HSV to RGB for smooth color transitions
            # Saturation = 1.0, Value = 0.5 for gentle colors
            c = 0.5  # Chroma (brightness)
            x = c * (1 - abs((hue / 60) % 2 - 1))
            
            if 0 <= hue < 60:
                r, g, b = c, x, 0
            elif 60 <= hue < 120:
                r, g, b = x, c, 0
            elif 120 <= hue < 180:
                r, g, b = 0, c, x
            elif 180 <= hue < 240:
                r, g, b = 0, x, c
            elif 240 <= hue < 300:
                r, g, b = x, 0, c
            else:  # 300 <= hue < 360
                r, g, b = c, 0, x
            
            # Convert to PWM duty cycle (0-100%)
            red_duty = r * 100
            green_duty = g * 100
            blue_duty = b * 100
            
            # Update PWM
            red_pwm.ChangeDutyCycle(red_duty)
            green_pwm.ChangeDutyCycle(green_duty)
            blue_pwm.ChangeDutyCycle(blue_duty)
            
            # Increment hue for next color
            hue += 0.5  # Slow color change
            if hue >= 360:
                hue = 0
            
            time.sleep(0.05)  # 20 FPS smooth animation
            
    except KeyboardInterrupt:
        print("\n🌈 Gentle colors stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cleanup_gpio(red_pwm, green_pwm, blue_pwm)
        print("✅ GPIO cleaned up safely")

if __name__ == "__main__":
    gentle_color_shift()
