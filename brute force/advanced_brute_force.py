"""
Enhanced Brute Force Tool with Visual Detection
==============================================

Advanced version with screen capture and visual recognition
for automatic success detection in 7 Days to Die.

This version can detect when a combination is successful by
analyzing the game screen for visual cues.
"""

import cv2
import numpy as np
import pyautogui
from PIL import Image
import time
import logging
from brute_force_bot import BruteForceBot

class AdvancedBruteForceBot(BruteForceBot):
    def __init__(self):
        super().__init__()
        self.success_detection_enabled = True
        self.reference_images = {}
        self.load_reference_images()
        
    def load_reference_images(self):
        """Load reference images for success detection"""
        try:
            # These would be screenshots of success indicators in the game
            # You would need to capture these manually first
            
            # Example: screenshot of "UNLOCKED" text or open container
            # self.reference_images['unlocked'] = cv2.imread('unlocked_reference.png')
            # self.reference_images['access_granted'] = cv2.imread('access_granted.png')
            
            self.logger.info("Reference images loaded for visual detection")
        except Exception as e:
            self.logger.warning(f"Could not load reference images: {e}")
            self.success_detection_enabled = False
            
    def take_screenshot(self, region=None):
        """Take screenshot of game area"""
        try:
            if region:
                # Screenshot specific region (x, y, width, height)
                screenshot = pyautogui.screenshot(region=region)
            else:
                # Full screen
                screenshot = pyautogui.screenshot()
                
            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return None
            
    def detect_success_visual(self):
        """
        Detect success using visual recognition
        Returns True if success is detected
        """
        if not self.success_detection_enabled:
            return False
            
        try:
            # Take screenshot of relevant area
            # You would need to adjust these coordinates for 7DTD interface
            screenshot = self.take_screenshot(region=(100, 100, 800, 600))
            if screenshot is None:
                return False
                
            # Convert to grayscale for template matching
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Check for success indicators
            for indicator_name, reference_img in self.reference_images.items():
                if reference_img is None:
                    continue
                    
                # Convert reference to grayscale
                gray_reference = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)
                
                # Template matching
                result = cv2.matchTemplate(gray_screenshot, gray_reference, cv2.TM_CCOEFF_NORMED)
                
                # Get the best match
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # If match confidence is high enough
                if max_val > 0.8:  # 80% confidence threshold
                    self.logger.info(f"Success detected: {indicator_name} (confidence: {max_val:.2f})")
                    return True
                    
            return False
            
        except Exception as e:
            self.logger.error(f"Error in visual detection: {e}")
            return False
            
    def detect_success_color(self):
        """
        Detect success by looking for specific color changes
        Useful if the interface changes color when unlocked
        """
        try:
            # Take screenshot of a specific area where color changes occur
            # Example: status indicator area
            screenshot = self.take_screenshot(region=(400, 300, 200, 100))
            if screenshot is None:
                return False
                
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for success indicators
            # Green color range (success)
            green_lower = np.array([40, 50, 50])
            green_upper = np.array([80, 255, 255])
            green_mask = cv2.inRange(hsv, green_lower, green_upper)
            
            # Count green pixels
            green_pixels = cv2.countNonZero(green_mask)
            total_pixels = screenshot.shape[0] * screenshot.shape[1]
            green_percentage = green_pixels / total_pixels
            
            # If more than 10% of the area is green, might indicate success
            if green_percentage > 0.1:
                self.logger.info(f"Green indicator detected: {green_percentage:.2f}% green pixels")
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error in color detection: {e}")
            return False
            
    def check_success(self):
        """
        Enhanced success detection using multiple methods
        """
        # Wait for the game to process the input
        time.sleep(1.5)
        
        # Method 1: Visual template matching
        if self.detect_success_visual():
            return True
            
        # Method 2: Color change detection
        if self.detect_success_color():
            return True
            
        # Method 3: Text recognition (OCR)
        if self.detect_success_text():
            return True
            
        return False
        
    def detect_success_text(self):
        """
        Use OCR to detect success text like "UNLOCKED", "ACCESS GRANTED", etc.
        Requires pytesseract: pip install pytesseract
        """
        try:
            import pytesseract
            
            # Take screenshot
            screenshot = self.take_screenshot(region=(200, 200, 600, 400))
            if screenshot is None:
                return False
                
            # Convert to PIL Image for OCR
            pil_image = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
            
            # Perform OCR
            text = pytesseract.image_to_string(pil_image).upper()
            
            # Check for success keywords
            success_keywords = ['UNLOCKED', 'ACCESS GRANTED', 'OPENED', 'SUCCESS', 'CORRECT']
            
            for keyword in success_keywords:
                if keyword in text:
                    self.logger.info(f"Success text detected: '{keyword}'")
                    return True
                    
            return False
            
        except ImportError:
            # pytesseract not installed
            return False
        except Exception as e:
            self.logger.error(f"Error in text detection: {e}")
            return False
            
    def calibrate_detection(self):
        """
        Calibration mode to help set up visual detection
        """
        print("\n" + "="*50)
        print("  VISUAL DETECTION CALIBRATION")
        print("="*50)
        print()
        print("This will help you set up automatic success detection.")
        print()
        print("Instructions:")
        print("1. Open 7 Days to Die")
        print("2. Navigate to a locked container")
        print("3. Enter a WRONG combination first")
        print("4. Press ENTER when ready to capture 'failed' state")
        
        input("Press ENTER when ready...")
        
        # Capture failed state
        failed_screenshot = self.take_screenshot()
        if failed_screenshot is not None:
            cv2.imwrite('failed_state.png', failed_screenshot)
            print("✓ Failed state captured")
            
        print()
        print("5. Now enter a CORRECT combination")
        print("6. Press ENTER when the container is unlocked")
        
        input("Press ENTER when container is unlocked...")
        
        # Capture success state
        success_screenshot = self.take_screenshot()
        if success_screenshot is not None:
            cv2.imwrite('success_state.png', success_screenshot)
            print("✓ Success state captured")
            
        print()
        print("Calibration complete!")
        print("Images saved: failed_state.png, success_state.png")
        print("You can now use these for reference in the main script.")

def main_advanced():
    """Main entry point for advanced version"""
    try:
        print("Advanced Brute Force Tool with Visual Detection")
        print("=" * 50)
        
        bot = AdvancedBruteForceBot()
        
        # Ask if user wants to calibrate first
        print("\nDo you want to run calibration mode first? (y/n): ", end="")
        if input().lower().startswith('y'):
            bot.calibrate_detection()
            return
            
        bot.run()
        
    except ImportError as e:
        print("Missing required dependencies for advanced features!")
        print("Please install with:")
        print("pip install opencv-python pillow numpy")
        print("Optional: pip install pytesseract (for text recognition)")
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error starting advanced application: {e}")

if __name__ == "__main__":
    main_advanced()
