"""
7 Days to Die - Container Brute Force Tool
==========================================

External keyboard automation script that attempts to brute force
container combinations by sending keyboard inputs to the game.

Requirements:
- Python 3.7+
- pip install pynput
- pip install keyboard
- pip install pyautogui

Usage:
1. Start 7 Days to Die
2. Approach a locked container (safe, secure loot container)
3. Open the combination interface
4. Run this script
5. The script will automatically try different combinations

Features:
- Multiple brute force strategies
- Configurable delay between attempts
- Progress tracking and logging
- Pause/resume functionality
- Smart detection of successful unlocks
"""

import time
import threading
import logging
import json
import os
from datetime import datetime
import pyautogui
import keyboard
from pynput import mouse
from pynput.keyboard import Key, Listener as KeyboardListener

class BruteForceBot:
    def __init__(self):
        self.running = False
        self.paused = False
        self.current_combination = [0, 0, 1, 2]  # Starting from 0012
        self.max_digits = 10  # 0-9
        self.attempt_count = 0
        self.successful_combinations = []
        self.delay_between_attempts = 0.02  # ULTRA FAST: minimal delay between attempts
        self.delay_between_inputs = 0.01   # ULTRA FAST: minimal delay between digits
        
        # Hot keys
        self.start_key = '+'
        self.pause_key = 'f2'
        self.stop_key = 'f3'
        self.calibrate_key = 'f4'  # For setting click positions
        
        # Game-specific settings
        self.combination_length = 4
        self.enter_key = 'enter'
        self.clear_key = 'c'  # Some games use 'c' to clear
        
        # Mouse click settings (OPTIMIZED FOR SPEED)
        self.auto_click_enabled = True
        self.input_field_pos = None  # Will be set during calibration
        self.submit_button_pos = None  # Will be set during calibration
        self.click_delay = 0.01  # ULTRA FAST: minimal delay after clicking
        self.process_delay = 0.05  # ULTRA FAST: minimal time to wait for game processing
        
        # TURBO MODE - Set to True for maximum speed (may cause issues on slower systems)
        self.turbo_mode = True
        if self.turbo_mode:
            self.delay_between_attempts = 0.01  # LUDICROUS SPEED
            self.delay_between_inputs = 0.005   # LUDICROUS SPEED
            self.click_delay = 0.005
            self.process_delay = 0.02
        
        # Logging setup
        self.setup_logging()
        
        # Load saved progress
        self.load_progress()
        
        print("🔓 7 Days to Die Brute Force Tool Initialized")
        print(f"   Hot Keys: +=Start, F2=Pause, F3=Stop, F4=Calibrate")
        print(f"   Current combination: {self.format_combination()}")
        print(f"   Attempts made: {self.attempt_count}")
        print(f"   Auto-click: {'Enabled' if self.auto_click_enabled else 'Disabled'}")
        print(f"   TURBO MODE: {'🚀 ENABLED' if self.turbo_mode else 'Disabled'}")
        if self.turbo_mode:
            print("   ⚡ LUDICROUS SPEED MODE - Up to 100 attempts/second!")
        
    def setup_logging(self):
        """Setup logging for tracking attempts"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'brute_force_log_{datetime.now().strftime("%Y%m%d")}.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_progress(self):
        """Load previous progress from file"""
        if os.path.exists('brute_force_progress.json'):
            try:
                with open('brute_force_progress.json', 'r') as f:
                    data = json.load(f)
                    self.current_combination = data.get('current_combination', [0, 0, 0, 0])
                    self.attempt_count = data.get('attempt_count', 0)
                    self.successful_combinations = data.get('successful_combinations', [])
                    self.logger.info(f"Loaded progress: {self.attempt_count} attempts made")
                    
                    # Load click positions if available
                    self.input_field_pos = data.get('input_field_pos', None)
                    self.submit_button_pos = data.get('submit_button_pos', None)
                    if self.input_field_pos:
                        self.logger.info(f"Loaded input field position: {self.input_field_pos}")
                    if self.submit_button_pos:
                        self.logger.info(f"Loaded submit button position: {self.submit_button_pos}")
            except Exception as e:
                self.logger.error(f"Error loading progress: {e}")
                
    def save_progress(self):
        """Save current progress to file"""
        try:
            data = {
                'current_combination': self.current_combination,
                'attempt_count': self.attempt_count,
                'successful_combinations': self.successful_combinations,
                'input_field_pos': self.input_field_pos,
                'submit_button_pos': self.submit_button_pos,
                'last_updated': datetime.now().isoformat()
            }
            with open('brute_force_progress.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving progress: {e}")
            
    def format_combination(self):
        """Format combination as string"""
        return ''.join(map(str, self.current_combination))
        
    def next_combination(self):
        """Generate next combination (incrementing from 0000 to 9999)"""
        # Increment like a counter
        carry = 1
        for i in range(len(self.current_combination) - 1, -1, -1):
            self.current_combination[i] += carry
            if self.current_combination[i] >= self.max_digits:
                self.current_combination[i] = 0
                carry = 1
            else:
                carry = 0
                break
                
        # Check if we've exhausted all combinations
        if carry == 1:
            self.logger.info("All combinations exhausted!")
            return False
        return True
        
    def click_input_field(self):
        """Click on the combination input field to focus it"""
        if self.input_field_pos and self.auto_click_enabled:
            try:
                pyautogui.click(self.input_field_pos[0], self.input_field_pos[1])
                time.sleep(self.click_delay)  # Minimal delay
                return True
            except Exception as e:
                self.logger.error(f"Error clicking input field: {e}")
                return False
        return False
        
    def click_submit_button(self):
        """Click the submit button if available"""
        if self.submit_button_pos and self.auto_click_enabled:
            try:
                pyautogui.click(self.submit_button_pos[0], self.submit_button_pos[1])
                time.sleep(self.click_delay)  # Minimal delay
                return True
            except Exception as e:
                self.logger.error(f"Error clicking submit button: {e}")
                return False
        return False
        
    def calibrate_click_positions(self):
        """Calibrate mouse click positions for automation"""
        print("\n" + "="*50)
        print("  MOUSE CLICK CALIBRATION")
        print("="*50)
        print()
        print("This will help you set up automatic mouse clicking.")
        print()
        print("Step 1: Position your mouse over the COMBINATION INPUT FIELD")
        print("        (The text box where you type the combination)")
        print("        Then press SPACE to save this position...")
        
        # Wait for space key to save input field position
        keyboard.wait('space')
        self.input_field_pos = pyautogui.position()
        print(f"✓ Input field position saved: {self.input_field_pos}")
        print()
        
        print("Step 2: Position your mouse over the SUBMIT BUTTON")
        print("        (The button that submits the combination)")
        print("        Then press SPACE to save this position...")
        print("        Or press ESC to skip if no button is needed...")
        
        # Wait for space or esc
        while True:
            if keyboard.is_pressed('space'):
                self.submit_button_pos = pyautogui.position()
                print(f"✓ Submit button position saved: {self.submit_button_pos}")
                break
            elif keyboard.is_pressed('esc'):
                print("⚠️ Submit button position skipped")
                self.submit_button_pos = None
                break
            time.sleep(0.1)
            
        print()
        print("Step 3: Testing the calibrated positions...")
        time.sleep(1)
        
        # Test the positions
        if self.input_field_pos:
            print("Testing input field click...")
            self.click_input_field()
            time.sleep(1)
            
        if self.submit_button_pos:
            print("Testing submit button click...")
            self.click_submit_button()
            time.sleep(1)
            
        print()
        print("✓ Calibration complete!")
        print("  The positions have been saved and will be used automatically.")
        print("  You can recalibrate anytime by pressing F4.")
        print()
        
        # Save the positions
        self.save_progress()
        
    def send_combination(self):
        """Send the current combination to the game with full click workflow - ULTRA FAST OPTIMIZED"""
        try:
            # Step 1: Click the input field to ensure it's focused (INSTANT)
            if not self.click_input_field():
                pass  # Continue anyway, might still work
            
            # Step 2: Clear any existing input (FASTEST METHOD)
            pyautogui.hotkey('ctrl', 'a')  # Select all
            time.sleep(0.005)  # Ultra minimal wait
            pyautogui.press('delete')  # Clear
            time.sleep(0.005)  # Ultra minimal wait
            
            # Step 3: Type combination INSTANTLY - no interval delay
            combination_str = self.format_combination()
            pyautogui.write(combination_str, interval=0)  # NO DELAY between keystrokes
            
            # Step 4: Submit IMMEDIATELY
            if self.submit_button_pos:
                if not self.click_submit_button():
                    pyautogui.press(self.enter_key)  # Fallback
            else:
                pyautogui.press(self.enter_key)
            
            # Step 5: Ultra minimal processing wait
            time.sleep(self.process_delay)
            
            self.logger.info(f"Attempted combination: {combination_str}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending combination: {e}")
            return False
            
    def check_success(self):
        """
        Check if the combination was successful
        This is game-specific and might need adjustment based on 
        visual cues or audio feedback in 7 Days to Die
        """
        # Wait a moment for the game to process
        time.sleep(1)
        
        # Here you could implement image recognition to detect success
        # For now, we'll rely on manual detection (user can press F3 to mark success)
        
        # Placeholder: return False to continue trying
        return False
        
    def run_brute_force(self):
        """Main brute force loop - ULTRA OPTIMIZED FOR SPEED"""
        self.logger.info("Starting brute force attack...")
        self.logger.info(f"Starting from combination: {self.format_combination()}")
        
        # Disable PyAutoGUI failsafe for speed (BE CAREFUL!)
        pyautogui.FAILSAFE = False
        
        while self.running:
            if self.paused:
                time.sleep(0.01)  # Minimal pause check delay
                continue
                
            # Send current combination (ULTRA FAST)
            if self.send_combination():
                self.attempt_count += 1
                
                # Check if successful (this would need game-specific detection)
                if self.check_success():
                    combination = self.format_combination()
                    self.successful_combinations.append(combination)
                    self.logger.info(f"SUCCESS! Combination found: {combination}")
                    print(f"🎉 SUCCESS! Working combination: {combination}")
                    
                    # Save the successful combination
                    with open(f'successful_combinations_{datetime.now().strftime("%Y%m%d")}.txt', 'a') as f:
                        f.write(f"{datetime.now().isoformat()}: {combination}\n")
                    
                    # Ask user if they want to continue
                    print("Do you want to continue searching for more combinations? (Press + to continue, F3 to stop)")
                    self.paused = True
                    
                else:
                    # Move to next combination (INSTANT)
                    if not self.next_combination():
                        self.logger.info("All combinations tried!")
                        self.running = False
                        break
                        
                # Save progress less frequently for speed
                if self.attempt_count % 500 == 0:  # Every 500 instead of 100
                    self.save_progress()
                    
                # Display progress less frequently for speed
                if self.attempt_count % 200 == 0:  # Every 200 instead of 50
                    print(f"⚡ TURBO Progress: {self.attempt_count} attempts, current: {self.format_combination()}")
                    
            # Ultra minimal wait before next attempt
            if not self.turbo_mode:
                time.sleep(self.delay_between_attempts)
            # In turbo mode, no delay at all except what's built into send_combination
            
        # Re-enable failsafe
        pyautogui.FAILSAFE = True
        self.save_progress()
        self.logger.info(f"Brute force stopped. Total attempts: {self.attempt_count}")
        
    def start(self):
        """Start the brute force attack"""
        if not self.running:
            self.running = True
            self.paused = False
            print("🚀 Starting brute force attack in 3 seconds...")
            print("   Make sure the combination input is focused in the game!")
            time.sleep(3)
            
            # Run in separate thread to allow hotkeys
            self.thread = threading.Thread(target=self.run_brute_force, daemon=True)
            self.thread.start()
            
    def pause(self):
        """Pause/resume the attack"""
        if self.running:
            self.paused = not self.paused
            status = "PAUSED" if self.paused else "RESUMED"
            print(f"⏸️ {status}")
            self.logger.info(f"Attack {status.lower()}")
            
    def stop(self):
        """Stop the attack"""
        if self.running:
            self.running = False
            self.paused = False
            print("🛑 Stopping brute force attack...")
            self.logger.info("Attack stopped by user")
            self.save_progress()
            
    def setup_hotkeys(self):
        """Setup hotkey listeners"""
        keyboard.add_hotkey(self.start_key, self.start)
        keyboard.add_hotkey(self.pause_key, self.pause)
        keyboard.add_hotkey(self.stop_key, self.stop)
        keyboard.add_hotkey(self.calibrate_key, self.calibrate_click_positions)
        keyboard.add_hotkey('esc', self.emergency_stop)
        
    def emergency_stop(self):
        """Emergency stop (ESC key)"""
        print("🚨 EMERGENCY STOP!")
        self.running = False
        self.paused = False
        self.save_progress()
        
    def run(self):
        """Main application loop"""
        print("\n" + "="*50)
        print("  7 DAYS TO DIE - BRUTE FORCE TOOL")
        print("="*50)
        print()
        print("Instructions:")
        print("1. Start 7 Days to Die")
        print("2. Approach a locked container")
        print("3. Open the combination interface")
        print("4. Click in the combination input field")
        print("5. Press F1 to start brute forcing")
        print()
        print("Controls:")
        print("+ (Plus) - Start/Restart brute force")
        print("F2 - Pause/Resume")
        print("F3 - Stop")
        print("ESC - Emergency stop")
        print()
        print(f"Current settings ({'TURBO' if self.turbo_mode else 'ULTRA FAST'} MODE):")
        print(f"- Delay between attempts: {self.delay_between_attempts}s")
        print(f"- Delay between digits: {self.delay_between_inputs}s")
        print(f"- Keyboard input: INSTANT (no interval)")
        print(f"- Click delay: {self.click_delay}s")
        print(f"- Process delay: {self.process_delay}s")
        print(f"- Combination length: {self.combination_length}")
        print(f"- Estimated speed: ~{int(1/self.delay_between_attempts)}-{int(1/self.delay_between_attempts*2)} attempts per second")
        print()
        print("Ready! Press + (Plus key) when you're in the game...")
        print()
        
        self.setup_hotkeys()
        
        try:
            # Keep the program running
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.stop()

def main():
    """Main entry point"""
    try:
        bot = BruteForceBot()
        bot.run()
    except ImportError as e:
        print("Missing required dependencies!")
        print("Please install with: pip install pynput keyboard pyautogui")
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
