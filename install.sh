#!/bin/bash
# PiRGB LED Controller Installation Script

echo "🌈 Installing PiRGB LED Controller..."

# Install dependencies
echo "Installing Python GPIO library..."
sudo apt update
sudo apt install -y python3-rpi.gpio python3-pip

# Set up permissions for GPIO access
echo "Setting up GPIO permissions..."
sudo usermod -a -G gpio $USER

# Make scripts executable
echo "Making scripts executable..."
chmod +x RGB/menu
find RGB -name "*.py" -exec chmod +x {} \;

# Create desktop shortcut (optional)
cat > ~/Desktop/PiRGB.desktop << 'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=PiRGB LED Controller
Comment=Control RGB LED with various effects
Exec=lxterminal -e "cd $HOME/RGB && ./menu"
Icon=applications-electronics
Terminal=true
Categories=Utility;Electronics;
DESKTOP

chmod +x ~/Desktop/PiRGB.desktop

echo "✅ Installation complete!"
echo ""
echo "🚀 To run PiRGB LED Controller:"
echo "   cd RGB"
echo "   ./menu"
echo ""
echo "💡 Make sure your RGB LED is connected to:"
echo "   Red:   GPIO 17 (Pin 11)"
echo "   Green: GPIO 27 (Pin 13)" 
echo "   Blue:  GPIO 22 (Pin 15)"
echo "   Ground: Any GND pin"
echo ""
echo "⚠️  Use appropriate resistors (220-330Ω recommended)"
