#!/usr/bin/env python3
"""
Safe RGB LED Controller
GPIO: Red=17, Green=27, Blue=22
"""
import RPi.GPIO as GPIO
import time
import math
import psutil
import signal
import sys

class RGBController:
    def __init__(self):
        # GPIO pins for RGB LED
        self.RED_PIN = 17
        self.GREEN_PIN = 27
        self.BLUE_PIN = 22
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup([self.RED_PIN, self.GREEN_PIN, self.BLUE_PIN], GPIO.OUT)
        
        # Create PWM objects for smooth color control
        self.red_pwm = GPIO.PWM(self.RED_PIN, 1000)  # 1kHz frequency
        self.green_pwm = GPIO.PWM(self.GREEN_PIN, 1000)
        self.blue_pwm = GPIO.PWM(self.BLUE_PIN, 1000)
        
        # Start PWM
        self.red_pwm.start(0)
        self.green_pwm.start(0)
        self.blue_pwm.start(0)
        
        self.running = True
        
        # Setup signal handlers for clean exit
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
    
    def set_color(self, r, g, b):
        """Set RGB color (0-100 for each channel)"""
        self.red_pwm.ChangeDutyCycle(r)
        self.green_pwm.ChangeDutyCycle(g)
        self.blue_pwm.ChangeDutyCycle(b)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB (0-100 scale)"""
        h = h / 360.0
        s = s / 100.0
        v = v / 100.0
        
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
        
        return int(r * 100), int(g * 100), int(b * 100)
    
    def color_shift(self):
        """Gentle color shifting effect"""
        print("Starting gentle color shift... Press Ctrl+C to stop")
        hue = 0
        while self.running:
            r, g, b = self.hsv_to_rgb(hue, 80, 50)  # Medium saturation, medium brightness
            self.set_color(r, g, b)
            hue = (hue + 1) % 360
            time.sleep(0.1)  # Slow, gentle shift
    
    def cpu_monitor(self):
        """RGB color based on CPU usage"""
        print("Starting CPU monitor... Press Ctrl+C to stop")
        print("Blue=Low CPU, Green=Medium CPU, Red=High CPU")
        
        while self.running:
            cpu_percent = psutil.cpu_percent(interval=0.5)
            
            if cpu_percent < 33:
                # Low CPU - Blue dominant
                r, g, b = int(cpu_percent * 1.5), 0, 100 - int(cpu_percent * 2)
            elif cpu_percent < 66:
                # Medium CPU - Green dominant
                cpu_adj = cpu_percent - 33
                r, g, b = int(cpu_adj * 2), 100 - int(cpu_adj), 0
            else:
                # High CPU - Red dominant
                cpu_adj = cpu_percent - 66
                r, g, b = 100, int((33 - cpu_adj) * 2), 0
            
            self.set_color(r, g, b)
            print(f"CPU: {cpu_percent:5.1f}% | RGB: ({r:3d}, {g:3d}, {b:3d})")
    
    def memory_monitor(self):
        """RGB color based on memory usage"""
        print("Starting memory monitor... Press Ctrl+C to stop")
        print("Green=Low Memory, Yellow=Medium Memory, Red=High Memory")
        
        while self.running:
            memory = psutil.virtual_memory()
            mem_percent = memory.percent
            
            if mem_percent < 50:
                # Low memory - Green
                r, g, b = 0, 100 - int(mem_percent), 0
            elif mem_percent < 80:
                # Medium memory - Yellow
                mem_adj = mem_percent - 50
                r, g, b = int(mem_adj * 3), 100, 0
            else:
                # High memory - Red
                mem_adj = mem_percent - 80
                r, g, b = 100, 100 - int(mem_adj * 5), 0
            
            self.set_color(r, g, b)
            print(f"Memory: {mem_percent:5.1f}% | RGB: ({r:3d}, {g:3d}, {b:3d})")
            time.sleep(1)
    
    def test_colors(self):
        """Test RGB functionality"""
        print("Testing RGB LED...")
        colors = [
            (100, 0, 0, "RED"),
            (0, 100, 0, "GREEN"), 
            (0, 0, 100, "BLUE"),
            (100, 100, 0, "YELLOW"),
            (100, 0, 100, "MAGENTA"),
            (0, 100, 100, "CYAN"),
            (100, 100, 100, "WHITE"),
            (0, 0, 0, "OFF")
        ]
        
        for r, g, b, name in colors:
            print(f"Setting color: {name}")
            self.set_color(r, g, b)
            time.sleep(1.5)
    
    def cleanup(self, signum=None, frame=None):
        """Clean shutdown"""
        print("\nShutting down RGB controller...")
        self.running = False
        self.set_color(0, 0, 0)  # Turn off LED
        self.red_pwm.stop()
        self.green_pwm.stop()
        self.blue_pwm.stop()
        GPIO.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    controller = RGBController()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "shift":
            controller.color_shift()
        elif mode == "cpu":
            controller.cpu_monitor()
        elif mode == "memory":
            controller.memory_monitor()
        elif mode == "test":
            controller.test_colors()
    else:
        print("Usage: python3 rgb_controller.py [shift|cpu|memory|test]")
    
    controller.cleanup()