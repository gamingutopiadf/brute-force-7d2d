#!/usr/bin/env python3
"""
7 Days to Die - Brute Force Tool GUI
===================================

A user-friendly GUI interface for the brute force container tool.
Built with tkinter for easy use and configuration.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
from datetime import datetime
import pyautogui
import keyboard
from brute_force_bot import BruteForceBot

class BruteForceGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("7 Days to Die - Brute Force Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure dark theme with green accents
        self.root.configure(bg='#0a0a0a')  # Very dark background
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Force clam theme for better dark theming
        
        # Create custom dark/green theme
        self.setup_dark_theme()
        
        # Force update all widget defaults to dark theme
        self.root.option_add('*TCombobox*Listbox.background', '#2a2a2a')
        self.root.option_add('*TCombobox*Listbox.foreground', '#e0e0e0')
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#00cc33')
        
                # Initialize the brute force bot
        from brute_force_bot import BruteForceBot
        self.bot = BruteForceBot()
        # Disable bot's own hotkeys since GUI handles them
        # (Don't call self.bot.setup_hotkeys())
        
        # Timing attributes for GUI updates
        self.last_attempt_time = time.time()
        self.last_attempt_count = 0
        self.is_running = False
        self.is_paused = False
        
        # Create GUI elements
        self.create_widgets()
        self.update_status()
        
        # Setup global hotkeys (after widgets are created)
        self.setup_hotkeys()
        
        # Start status update loop
        self.root.after(100, self.status_update_loop)
        
    def setup_dark_theme(self):
        """Configure dark green/black theme"""
        
        # Dark background colors
        dark_bg = '#0a0a0a'      # Very dark background
        frame_bg = '#1a1a1a'     # Slightly lighter for frames
        entry_bg = '#2a2a2a'     # Entry field background
        
        # Green accent colors
        green_light = '#00ff41'   # Bright matrix green
        green_medium = '#00cc33'  # Medium green
        green_dark = '#008822'    # Dark green
        
        # Text colors
        text_light = '#e0e0e0'    # Light text
        text_green = '#00ff41'    # Green text
        
        # Configure ttk styles
        self.style.configure('TFrame', background=frame_bg, borderwidth=1, relief='solid')
        self.style.configure('TLabelFrame', background=frame_bg, foreground=green_light, 
                            borderwidth=2, relief='solid')
        self.style.configure('TLabelFrame.Label', background=frame_bg, foreground=green_light,
                            font=('Arial', 10, 'bold'))
        
        self.style.configure('TLabel', background=frame_bg, foreground=text_light)
        self.style.configure('TEntry', background=entry_bg, foreground=text_light,
                            fieldbackground=entry_bg, borderwidth=1, relief='solid',
                            insertcolor=text_green)
        self.style.configure('TCombobox', background=entry_bg, foreground=text_light,
                            fieldbackground=entry_bg, borderwidth=1, relief='solid',
                            insertcolor=text_green, selectbackground=green_dark)
        self.style.configure('TCheckbutton', background=frame_bg, foreground=text_light,
                            focuscolor='none')
        
        # Map styles for different states to prevent white backgrounds
        self.style.map('TEntry',
                      fieldbackground=[('focus', entry_bg),
                                     ('!focus', entry_bg),
                                     ('active', entry_bg),
                                     ('disabled', entry_bg)])
        self.style.map('TCombobox',
                      fieldbackground=[('focus', entry_bg),
                                     ('!focus', entry_bg),
                                     ('readonly', entry_bg),
                                     ('active', entry_bg),
                                     ('disabled', entry_bg)],
                      selectbackground=[('focus', green_dark),
                                      ('!focus', green_dark)])
        self.style.map('TLabelFrame',
                      background=[('active', frame_bg),
                                ('!active', frame_bg)])
        
        # Override combobox popup styling
        self.style.configure('TCombobox.Listbox',
                            background=entry_bg,
                            foreground=text_light,
                            selectbackground=green_dark)
        
        # Button styles
        self.style.configure('TButton', 
                            background=green_dark, 
                            foreground='white',
                            borderwidth=2,
                            relief='raised',
                            font=('Arial', 9, 'bold'))
        self.style.map('TButton',
                      background=[('active', green_medium),
                                ('pressed', green_light)])
        
        # Special button styles
        self.style.configure('Start.TButton',
                            background=green_medium,
                            foreground='black',
                            font=('Arial', 10, 'bold'))
        self.style.map('Start.TButton',
                      background=[('active', green_light)])
        
        self.style.configure('Stop.TButton',
                            background='#cc0000',
                            foreground='white',
                            font=('Arial', 10, 'bold'))
        self.style.map('Stop.TButton',
                      background=[('active', '#ff0000')])
        
        self.style.configure('Pause.TButton',
                            background='#ff8800',
                            foreground='black',
                            font=('Arial', 10, 'bold'))
        self.style.map('Pause.TButton',
                      background=[('active', '#ffaa00')])
        
        # Progress bar
        self.style.configure('TProgressbar',
                            background=green_medium,
                            troughcolor=entry_bg,
                            borderwidth=1,
                            relief='solid')
        
        # Scrolled text (for log)
        self.log_style = {
            'bg': dark_bg,
            'fg': green_light,
            'insertbackground': green_light,
            'selectbackground': green_dark,
            'selectforeground': 'white',
            'font': ('Courier', 9)
        }
        
        # Title label style
        self.style.configure('Title.TLabel', 
                            background=frame_bg, 
                            foreground=green_light,
                            font=('Arial', 16, 'bold'))
        
    def setup_hotkeys(self):
        """Setup global hotkeys for start/stop functionality"""
        try:
            # Hotkey to start brute force (F9)
            keyboard.add_hotkey('f9', self.hotkey_start)
            
            # Hotkey to stop brute force (F10)
            keyboard.add_hotkey('f10', self.hotkey_stop)
            
            # Hotkey to pause/resume brute force (F11)
            keyboard.add_hotkey('f11', self.hotkey_pause)
            
            # Hotkey to mark current combination as successful (F12)
            keyboard.add_hotkey('f12', self.hotkey_mark_success)
            
            # Hotkey to clear correct password (Shift+F12)
            keyboard.add_hotkey('shift+f12', self.hotkey_clear_correct)
            
            # Emergency stop (Ctrl+F12)
            keyboard.add_hotkey('ctrl+f12', self.hotkey_emergency_stop)
            
            self.log_message("🎮 Hotkeys registered:")
            self.log_message("  F9  - Start brute force")
            self.log_message("  F10 - Stop brute force")
            self.log_message("  F11 - Pause/Resume")
            self.log_message("  F12 - Mark combination as correct")
            self.log_message("  Shift+F12 - Clear correct password")
            self.log_message("  Ctrl+F12 - Emergency stop")
            
        except Exception as e:
            self.log_message(f"⚠️ Failed to register hotkeys: {e}")
    
    def hotkey_start(self):
        """Hotkey handler for starting brute force"""
        if not self.is_running:
            self.log_message("🎮 F9 pressed - Starting brute force...")
            self.root.after(0, self.start_brute_force)
        else:
            self.log_message("🎮 F9 pressed - Already running!")
            
    def hotkey_stop(self):
        """Hotkey handler for stopping brute force"""
        if self.is_running:
            self.log_message("🎮 F10 pressed - Stopping brute force...")
            self.root.after(0, self.stop_brute_force)
        else:
            self.log_message("🎮 F10 pressed - Not running!")
            
    def hotkey_pause(self):
        """Hotkey handler for pausing/resuming brute force"""
        if self.is_running:
            if self.is_paused:
                self.log_message("🎮 F11 pressed - Resuming...")
            else:
                self.log_message("🎮 F11 pressed - Pausing...")
            self.root.after(0, self.pause_brute_force)
        else:
            self.log_message("🎮 F11 pressed - Not running!")
            
    def hotkey_mark_success(self):
        """Hotkey handler for marking current combination as successful"""
        if self.bot and hasattr(self.bot, 'current_combination'):
            current_combo = ''.join(map(str, self.bot.current_combination))
            self.log_message(f"🎉 F12 pressed - Marking {current_combo} as CORRECT!")
            self.root.after(0, lambda: self.mark_combination_successful(current_combo))
        else:
            self.log_message("🎮 F12 pressed - No combination to mark!")
            
    def hotkey_clear_correct(self):
        """Hotkey handler for clearing correct password"""
        self.log_message("🗑️ Shift+F12 pressed - Clearing correct password...")
        self.root.after(0, self.clear_correct_password)
            
    def mark_combination_successful(self, combination):
        """Mark a combination as successful"""
        if self.bot:
            # Add to successful combinations if not already there
            if combination not in self.bot.successful_combinations:
                self.bot.successful_combinations.append(combination)
                self.correct_password_var.set(combination)
                self.log_message(f"✅ Password {combination} marked as CORRECT!")
                
                # Save the successful combination to file
                try:
                    with open(f'successful_combinations_{datetime.now().strftime("%Y%m%d")}.txt', 'a') as f:
                        f.write(f"{datetime.now().isoformat()}: {combination}\n")
                except Exception as e:
                    self.log_message(f"⚠️ Error saving to file: {e}")
                
                # Save progress
                self.bot.save_progress()
                
                # Pause the brute force to give user time to verify
                if self.is_running:
                    self.is_paused = True
                    if self.bot:
                        self.bot.paused = True
                    self.log_message("⏸️ Brute force paused - Press F11 to resume or F10 to stop")
            else:
                self.log_message(f"⚠️ Password {combination} already marked as correct!")
            
    def hotkey_emergency_stop(self):
        """Emergency stop hotkey handler"""
        self.log_message("🚨 CTRL+F12 pressed - EMERGENCY STOP!")
        self.root.after(0, self.emergency_stop)
        
    def emergency_stop(self):
        """Emergency stop function"""
        self.is_running = False
        self.is_paused = False
        if self.bot:
            self.bot.running = False
            self.bot.paused = False
        self.log_message("🚨 EMERGENCY STOP activated!")
        self.update_status()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="news")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title with green styling
        title_label = ttk.Label(main_frame, text="🔓 7 Days to Die - Brute Force Tool", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # === CONFIGURATION SECTION ===
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Starting combination
        ttk.Label(config_frame, text="Starting Combination:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.start_combo_var = tk.StringVar(value="0012")
        start_combo_entry = ttk.Entry(config_frame, textvariable=self.start_combo_var, width=10)
        start_combo_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Speed settings
        ttk.Label(config_frame, text="Speed Mode:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.speed_var = tk.StringVar(value="Turbo")
        speed_combo = ttk.Combobox(config_frame, textvariable=self.speed_var, 
                                  values=["Normal", "Fast", "Turbo", "Ludicrous"], width=12)
        speed_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        speed_combo.state(['readonly'])
        
        # Auto-click enabled
        self.auto_click_var = tk.BooleanVar(value=True)
        auto_click_check = ttk.Checkbutton(config_frame, text="Enable Auto-Click", 
                                          variable=self.auto_click_var)
        auto_click_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # === MOUSE CALIBRATION SECTION ===
        calib_frame = ttk.LabelFrame(main_frame, text="Mouse Calibration", padding="10")
        calib_frame.grid(row=2, column=0, columnspan=2, sticky="we", pady=(0, 10))
        calib_frame.columnconfigure(2, weight=1)
        
        # Input field position
        ttk.Label(calib_frame, text="Input Field:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.input_pos_var = tk.StringVar(value="Not Set")
        ttk.Label(calib_frame, textvariable=self.input_pos_var).grid(row=0, column=1, sticky=tk.W, padx=(5, 10), pady=2)
        ttk.Button(calib_frame, text="Calibrate Input", 
                  command=self.calibrate_input).grid(row=0, column=2, sticky=tk.E, pady=2)
        
        # Submit button position
        ttk.Label(calib_frame, text="Submit Button:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.submit_pos_var = tk.StringVar(value="Not Set")
        ttk.Label(calib_frame, textvariable=self.submit_pos_var).grid(row=1, column=1, sticky=tk.W, padx=(5, 10), pady=2)
        ttk.Button(calib_frame, text="Calibrate Submit", 
                  command=self.calibrate_submit).grid(row=1, column=2, sticky=tk.E, pady=2)
        
        # === HOTKEY INFORMATION ===
        hotkey_frame = ttk.LabelFrame(main_frame, text="Global Hotkeys", padding="10")
        hotkey_frame.grid(row=2, column=2, sticky="we", padx=(10, 0), pady=(0, 10))
        
        ttk.Label(hotkey_frame, text="F9 - Start", font=('Courier', 9)).grid(row=0, column=0, sticky=tk.W, pady=1)
        ttk.Label(hotkey_frame, text="F10 - Stop", font=('Courier', 9)).grid(row=1, column=0, sticky=tk.W, pady=1)
        ttk.Label(hotkey_frame, text="F11 - Pause", font=('Courier', 9)).grid(row=2, column=0, sticky=tk.W, pady=1)
        ttk.Label(hotkey_frame, text="F12 - Mark Correct", font=('Courier', 9)).grid(row=3, column=0, sticky=tk.W, pady=1)
        ttk.Label(hotkey_frame, text="Shift+F12 - Clear", font=('Courier', 9)).grid(row=4, column=0, sticky=tk.W, pady=1)
        ttk.Label(hotkey_frame, text="Ctrl+F12 - Emergency", font=('Courier', 9)).grid(row=5, column=0, sticky=tk.W, pady=1)
        
        # === CONTROL SECTION ===
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=3, column=0, columnspan=3, sticky="we", pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, columnspan=3, pady=5)
        
        self.start_btn = ttk.Button(button_frame, text="🚀 START", command=self.start_brute_force,
                                   style='Start.TButton')
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = ttk.Button(button_frame, text="⏸️ PAUSE", command=self.pause_brute_force,
                                   state='disabled', style='Pause.TButton')
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="🛑 STOP", command=self.stop_brute_force,
                                  state='disabled', style='Stop.TButton')
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        self.test_btn = ttk.Button(button_frame, text="🧪 TEST", command=self.test_positions)
        self.test_btn.grid(row=0, column=3, padx=5)
        
        self.mark_correct_btn = ttk.Button(button_frame, text="✅ MARK CORRECT", 
                                          command=self.mark_current_combination_correct,
                                          style='Start.TButton')
        self.mark_correct_btn.grid(row=0, column=4, padx=5)
        
        self.clear_correct_btn = ttk.Button(button_frame, text="🗑️ CLEAR CORRECT", 
                                           command=self.clear_correct_password,
                                           style='Stop.TButton')
        self.clear_correct_btn.grid(row=0, column=5, padx=5)
        
        # === STATUS SECTION ===
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=3, sticky="we", pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        # Status display
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=('Arial', 10, 'bold'))
        status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(status_frame, text="Current Combination:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.current_combo_var = tk.StringVar(value="0012")
        ttk.Label(status_frame, textvariable=self.current_combo_var, font=('Courier', 12, 'bold')).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(status_frame, text="Attempts Made:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.attempts_var = tk.StringVar(value="0")
        ttk.Label(status_frame, textvariable=self.attempts_var, font=('Arial', 10, 'bold')).grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(status_frame, text="Speed:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.speed_display_var = tk.StringVar(value="0 attempts/sec")
        ttk.Label(status_frame, textvariable=self.speed_display_var).grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Progress bar
        ttk.Label(status_frame, text="Progress:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=10000)
        self.progress_bar.grid(row=4, column=1, sticky="we", padx=(5, 0), pady=2)
        
        # Progress percentage label
        self.progress_percent_var = tk.StringVar(value="0.00%")
        ttk.Label(status_frame, textvariable=self.progress_percent_var, font=('Arial', 9)).grid(row=4, column=2, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Correct password field
        ttk.Label(status_frame, text="Correct Password:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.correct_password_var = tk.StringVar(value="Not Found")
        correct_password_label = ttk.Label(status_frame, textvariable=self.correct_password_var, 
                                          font=('Courier', 12, 'bold'), foreground='#00ff41')
        correct_password_label.grid(row=5, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # === LOG SECTION ===
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky="news", pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Log text area with dark theme
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD,
                                                 bg='#0a0a0a', fg='#00ff41',
                                                 insertbackground='#00ff41',
                                                 selectbackground='#1a4f1a',
                                                 font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky="news")
        
        # Clear log button
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).grid(row=1, column=0, pady=(5, 0))
        
        # Configure button styles
        self.style.configure('Success.TButton', foreground='green')
        
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
        
    def calibrate_input(self):
        """Calibrate input field position"""
        self.log_message("Position mouse over INPUT FIELD and press SPACE...")
        messagebox.showinfo("Calibration", "Position your mouse over the COMBINATION INPUT FIELD and press SPACE")
        
        def wait_for_space():
            keyboard.wait('space')
            pos = pyautogui.position()
            self.input_pos_var.set(f"({pos.x}, {pos.y})")
            self.log_message(f"Input field position set: {pos}")
            if self.bot:
                self.bot.input_field_pos = (pos.x, pos.y)
                self.bot.save_progress()
                
        threading.Thread(target=wait_for_space, daemon=True).start()
        
    def calibrate_submit(self):
        """Calibrate submit button position"""
        self.log_message("Position mouse over SUBMIT BUTTON and press SPACE...")
        messagebox.showinfo("Calibration", "Position your mouse over the SUBMIT BUTTON and press SPACE")
        
        def wait_for_space():
            keyboard.wait('space')
            pos = pyautogui.position()
            self.submit_pos_var.set(f"({pos.x}, {pos.y})")
            self.log_message(f"Submit button position set: {pos}")
            if self.bot:
                self.bot.submit_button_pos = (pos.x, pos.y)
                self.bot.save_progress()
                
        threading.Thread(target=wait_for_space, daemon=True).start()
        
    def test_positions(self):
        """Test the calibrated positions"""
        if not self.bot:
            self.init_bot()
            
        self.log_message("Testing calibrated positions...")
        
        def test():
            try:
                if self.bot.input_field_pos:
                    self.log_message("Clicking input field...")
                    self.bot.click_input_field()
                    time.sleep(1)
                    
                if self.bot.submit_button_pos:
                    self.log_message("Clicking submit button...")
                    self.bot.click_submit_button()
                    time.sleep(1)
                    
                self.log_message("Position test complete!")
            except Exception as e:
                self.log_message(f"Test error: {e}")
                
        threading.Thread(target=test, daemon=True).start()
        
    def mark_current_combination_correct(self):
        """Mark the current combination as correct via button click"""
        if self.bot and hasattr(self.bot, 'current_combination'):
            current_combo = ''.join(map(str, self.bot.current_combination))
            self.log_message(f"🎉 Button pressed - Marking {current_combo} as CORRECT!")
            self.mark_combination_successful(current_combo)
        else:
            self.log_message("❌ No current combination to mark!")
            
    def clear_correct_password(self):
        """Clear the correct password field and reset successful combinations"""
        if self.bot and hasattr(self.bot, 'successful_combinations') and self.bot.successful_combinations:
            # Ask for confirmation
            from tkinter import messagebox
            confirmed = messagebox.askyesno("Clear Correct Password", 
                                          f"Are you sure you want to clear the correct password?\n\n"
                                          f"Current password: {self.correct_password_var.get()}\n\n"
                                          f"This will remove all successful combinations.")
            
            if confirmed:
                # Clear the successful combinations list
                self.bot.successful_combinations.clear()
                
                # Reset the display
                self.correct_password_var.set("Not Found")
                
                # Log the action
                self.log_message("🗑️ Correct password cleared!")
                
                # Save the updated progress (without successful combinations)
                self.bot.save_progress()
            else:
                self.log_message("❌ Clear operation cancelled!")
        elif self.bot and hasattr(self.bot, 'successful_combinations') and not self.bot.successful_combinations:
            self.log_message("❌ No password to clear!")
        else:
            self.log_message("❌ No bot initialized!")
        
    def init_bot(self):
        """Initialize the brute force bot"""
        if not self.bot:
            self.bot = BruteForceBot()
            
            # Apply GUI settings to bot
            start_combo = self.start_combo_var.get()
            if len(start_combo) == 4 and start_combo.isdigit():
                self.bot.current_combination = [int(d) for d in start_combo]
                
            # Apply speed settings
            speed_mode = self.speed_var.get()
            if speed_mode == "Normal":
                self.bot.delay_between_attempts = 0.5
                self.bot.delay_between_inputs = 0.1
            elif speed_mode == "Fast":
                self.bot.delay_between_attempts = 0.1
                self.bot.delay_between_inputs = 0.05
            elif speed_mode == "Turbo":
                self.bot.delay_between_attempts = 0.02
                self.bot.delay_between_inputs = 0.01
            elif speed_mode == "Ludicrous":
                self.bot.delay_between_attempts = 0.01
                self.bot.delay_between_inputs = 0.005
                
            self.bot.auto_click_enabled = self.auto_click_var.get()
            
    def start_brute_force(self):
        """Start the brute force attack"""
        if not self.is_running:
            self.init_bot()
            
            self.is_running = True
            self.is_paused = False
            
            # Update button states
            self.start_btn.config(state='disabled')
            self.pause_btn.config(state='normal')
            self.stop_btn.config(state='normal')
            
            self.log_message("🚀 Starting brute force attack...")
            
            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            
    def run_bot(self):
        """Run the bot (called in separate thread)"""
        try:
            self.bot.running = True
            self.bot.paused = False
            
            # Override bot's run_brute_force method to work with GUI
            while self.bot.running and self.is_running:
                if self.bot.paused or self.is_paused:
                    time.sleep(0.1)
                    continue
                    
                # Send combination
                if self.bot.send_combination():
                    self.bot.attempt_count += 1
                    
                    # Move to next combination
                    if not self.bot.next_combination():
                        self.log_message("All combinations exhausted!")
                        break
                        
                    # Save progress periodically
                    if self.bot.attempt_count % 100 == 0:
                        self.bot.save_progress()
                        
                time.sleep(self.bot.delay_between_attempts)
                
        except Exception as e:
            self.log_message(f"Error: {e}")
        finally:
            self.is_running = False
            
    def pause_brute_force(self):
        """Pause/resume the brute force attack"""
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.bot:
                self.bot.paused = self.is_paused
                
            status = "PAUSED" if self.is_paused else "RESUMED"
            self.pause_btn.config(text=f"▶️ RESUME" if self.is_paused else "⏸️ PAUSE")
            self.log_message(f"⏸️ {status}")
            
    def stop_brute_force(self):
        """Stop the brute force attack"""
        if self.is_running:
            self.is_running = False
            if self.bot:
                self.bot.running = False
                self.bot.save_progress()
                
            # Update button states
            self.start_btn.config(state='normal')
            self.pause_btn.config(state='disabled', text="⏸️ PAUSE")
            self.stop_btn.config(state='disabled')
            
            self.log_message("🛑 Brute force attack stopped")
            
    def update_status(self):
        """Update status display"""
        if self.is_running:
            if self.is_paused:
                self.status_var.set("⏸️ PAUSED")
            else:
                self.status_var.set("🚀 RUNNING")
        else:
            self.status_var.set("⭕ READY")
            
        if self.bot:
            combo_str = ''.join(map(str, self.bot.current_combination))
            self.current_combo_var.set(combo_str)
            self.attempts_var.set(str(self.bot.attempt_count))
            
            # Calculate progress based on current combination position
            # Convert current combination to decimal number to get position
            current_number = 0
            for i, digit in enumerate(self.bot.current_combination):
                current_number += digit * (10 ** (len(self.bot.current_combination) - 1 - i))
            
            # Total possible combinations (0000 to 9999 = 10000 combinations)
            total_combinations = 10 ** self.bot.combination_length
            
            # Calculate progress percentage
            progress_percent = (current_number / total_combinations) * 100
            self.progress_var.set(min(progress_percent, 100))
            self.progress_percent_var.set(f"{progress_percent:.2f}%")
            
            # Check if we found a successful combination
            if hasattr(self.bot, 'successful_combinations') and self.bot.successful_combinations:
                if self.bot.successful_combinations[-1] != self.correct_password_var.get():
                    self.correct_password_var.set(self.bot.successful_combinations[-1])
                    self.log_message(f"🎉 SUCCESS! Password found: {self.bot.successful_combinations[-1]}")
            
            # Calculate speed
            current_time = time.time()
            if current_time - self.last_attempt_time > 1:  # Update every second
                attempts_per_sec = (self.bot.attempt_count - self.last_attempt_count) / (current_time - self.last_attempt_time)
                self.speed_display_var.set(f"{attempts_per_sec:.1f} attempts/sec")
                self.last_attempt_time = current_time
                self.last_attempt_count = self.bot.attempt_count
                    
    def status_update_loop(self):
        """Continuous status update loop"""
        self.update_status()
        self.root.after(500, self.status_update_loop)  # Update every 500ms
        
    def run(self):
        """Start the GUI"""
        self.log_message("🔓 7 Days to Die Brute Force Tool initialized")
        self.log_message("1. Configure settings above")
        self.log_message("2. Calibrate mouse positions")
        self.log_message("3. Open 7DTD and navigate to locked container")
        self.log_message("4. Click START to begin brute forcing")
        
        # Setup cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing"""
        try:
            # Stop any running processes
            self.is_running = False
            if self.bot:
                self.bot.running = False
            
            # Unregister hotkeys
            keyboard.unhook_all()
            if hasattr(self, 'log_text'):
                self.log_message("🎮 Hotkeys unregistered")
            else:
                print("🎮 Hotkeys unregistered")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            self.root.destroy()

def main():
    """Main entry point"""
    try:
        app = BruteForceGUI()
        app.run()
    except ImportError as e:
        messagebox.showerror("Missing Dependencies", 
                           f"Missing required packages!\n\nPlease install:\npip install pynput keyboard pyautogui\n\nError: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application:\n{e}")

if __name__ == "__main__":
    main()
