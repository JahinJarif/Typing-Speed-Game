import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import time
import threading

class TypingSpeedGame:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Typing Speed Master")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0f1419")
        self.root.resizable(True, True)
        
        # Set window icon and style
        try:
            self.root.iconname("⚡")
        except:
            pass
            
        # Configure modern styling
        self.setup_styles()
        
        # Game variables
        self.current_text = ""
        self.start_time = None
        self.end_time = None
        self.time_limit = 120  # Default 2 minutes
        self.timer_running = False
        self.remaining_time = 0
        self.correct_chars = 0
        self.total_chars = 0
        self.current_position = 0
        
        # Word lists for different difficulty levels
        self.word_lists = {
            "Easy": [
                "cat", "dog", "run", "jump", "walk", "talk", "book", "read", "write", "play",
                "game", "time", "work", "home", "food", "love", "life", "help", "good", "best",
                "make", "take", "come", "look", "feel", "know", "think", "first", "last", "find",
                "give", "hand", "part", "place", "right", "great", "small", "large", "world", "state"
            ],
            "Medium": [
                "computer", "keyboard", "monitor", "programming", "development", "application", "function",
                "variable", "language", "algorithm", "structure", "database", "network", "security",
                "interface", "technology", "innovation", "creativity", "productivity", "efficiency",
                "organization", "management", "communication", "collaboration", "implementation",
                "optimization", "configuration", "documentation", "maintenance", "troubleshooting"
            ],
            "Hard": [
                "extraordinary", "incomprehensible", "disproportionate", "responsibilities", "characteristics",
                "administration", "transformation", "establishment", "implementation", "acknowledgment",
                "representative", "infrastructure", "standardization", "internationalization",
                "multidisciplinary", "telecommunications", "entrepreneurship", "simultaneously",
                "consciousness", "philosophical", "psychological", "technological", "environmental",
                "organizational", "constitutional", "revolutionary", "extraordinary", "fundamentally"
            ]
        }
        
        self.setup_ui()
    
    def setup_styles(self):
        """Setup modern styling and fonts"""
        # Create custom fonts
        try:
            self.title_font = font.Font(family="SF Pro Display", size=28, weight="bold")
            self.heading_font = font.Font(family="SF Pro Display", size=16, weight="bold")
            self.body_font = font.Font(family="SF Pro Text", size=12)
            self.mono_font = font.Font(family="SF Mono", size=14)
            self.stat_font = font.Font(family="SF Pro Display", size=14, weight="bold")
        except:
            # Fallback fonts for cross-platform compatibility
            self.title_font = font.Font(family="Arial", size=28, weight="bold")
            self.heading_font = font.Font(family="Arial", size=16, weight="bold")
            self.body_font = font.Font(family="Arial", size=12)
            self.mono_font = font.Font(family="Courier", size=14)
            self.stat_font = font.Font(family="Arial", size=14, weight="bold")
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom button style
        style.configure('Modern.TButton',
                       background='#00d4aa',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        style.map('Modern.TButton',
                 background=[('active', '#00b894'),
                           ('pressed', '#00a085')])
        
        # Custom combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground='#2d3748',
                       background='#2d3748',
                       foreground='white',
                       borderwidth=0,
                       arrowcolor='#00d4aa')
        
        # Colors palette
        self.colors = {
            'bg_primary': '#0f1419',
            'bg_secondary': '#1a202c',
            'bg_tertiary': '#2d3748',
            'accent': '#00d4aa',
            'accent_hover': '#00b894',
            'text_primary': '#ffffff',
            'text_secondary': '#a0aec0',
            'success': '#48bb78',
            'warning': '#ed8936',
            'error': '#f56565',
            'info': '#4299e1'
        }
        
    def setup_ui(self):
        # Create main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header section with gradient-like effect
        header_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Title with emoji and modern styling
        title_label = tk.Label(
            header_frame, 
            text="⚡ Typing Speed Master", 
            font=self.title_font, 
            bg=self.colors['bg_primary'], 
            fg=self.colors['accent']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Test your typing speed and accuracy with style",
            font=self.body_font,
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Settings section with modern card design
        settings_card = tk.Frame(main_container, bg=self.colors['bg_secondary'], relief="flat")
        settings_card.pack(fill="x", pady=(0, 20))
        
        # Add subtle border effect
        border_frame = tk.Frame(settings_card, bg=self.colors['accent'], height=3)
        border_frame.pack(fill="x")
        
        settings_content = tk.Frame(settings_card, bg=self.colors['bg_secondary'])
        settings_content.pack(fill="x", padx=30, pady=20)
        
        # Settings title
        settings_title = tk.Label(
            settings_content,
            text="🎯 Game Settings",
            font=self.heading_font,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        settings_title.pack(anchor="w", pady=(0, 15))
        
        # Settings controls in a grid
        controls_frame = tk.Frame(settings_content, bg=self.colors['bg_secondary'])
        controls_frame.pack(fill="x")
        
        # Difficulty selection with icons
        diff_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        diff_frame.pack(side="left", padx=(0, 40))
        
        tk.Label(
            diff_frame, 
            text="🎮 Difficulty Level:", 
            font=self.body_font, 
            bg=self.colors['bg_secondary'], 
            fg=self.colors['text_primary']
        ).pack(anchor="w")
        
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_combo = ttk.Combobox(
            diff_frame, 
            textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=12,
            font=self.body_font,
            style='Modern.TCombobox'
        )
        difficulty_combo.pack(pady=(5, 0))
        
        # Time limit selection with icons
        time_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        time_frame.pack(side="left", padx=(0, 40))
        
        tk.Label(
            time_frame, 
            text="⏱️ Time Limit:", 
            font=self.body_font, 
            bg=self.colors['bg_secondary'], 
            fg=self.colors['text_primary']
        ).pack(anchor="w")
        
        self.time_var = tk.StringVar(value="2 minutes")
        time_combo = ttk.Combobox(
            time_frame, 
            textvariable=self.time_var,
            values=["2 minutes", "3 minutes"],
            state="readonly",
            width=12,
            font=self.body_font,
            style='Modern.TCombobox'
        )
        time_combo.pack(pady=(5, 0))
        
        # Start button with modern styling
        button_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        button_frame.pack(side="right")
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Start Game",
            font=self.heading_font,
            bg=self.colors['accent'],
            fg="white",
            command=self.start_game,
            padx=30,
            pady=15,
            border=0,
            cursor="hand2",
            activebackground=self.colors['accent_hover'],
            activeforeground="white",
            relief="flat"
        )
        self.start_button.pack()
        
        # Timer section with circular design concept
        timer_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'])
        timer_frame.pack(fill="x", pady=(0, 20))
        
        timer_border = tk.Frame(timer_frame, bg=self.colors['warning'], height=3)
        timer_border.pack(fill="x")
        
        timer_content = tk.Frame(timer_frame, bg=self.colors['bg_secondary'])
        timer_content.pack(pady=15)
        
        self.timer_label = tk.Label(
            timer_content,
            text="⏰ Time: 2:00",
            font=font.Font(family="Arial", size=20, weight="bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['warning']
        )
        self.timer_label.pack()
        
        # Text display section with modern card design
        text_card = tk.Frame(main_container, bg=self.colors['bg_secondary'], relief="flat")
        text_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Text card header
        text_header = tk.Frame(text_card, bg=self.colors['info'], height=3)
        text_header.pack(fill="x")
        
        text_title_frame = tk.Frame(text_card, bg=self.colors['bg_secondary'])
        text_title_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            text_title_frame,
            text="📝 Text to Type",
            font=self.heading_font,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(side="left")
        
        # Text display with scrollbar
        text_content = tk.Frame(text_card, bg=self.colors['bg_secondary'])
        text_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create text widget with scrollbar
        text_scroll_frame = tk.Frame(text_content, bg=self.colors['bg_secondary'])
        text_scroll_frame.pack(fill="both", expand=True)
        
        self.text_display = tk.Text(
            text_scroll_frame,
            font=self.mono_font,
            wrap="word",
            height=8,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            state="disabled",
            cursor="arrow",
            selectbackground=self.colors['accent'],
            insertbackground=self.colors['accent'],
            border=0,
            padx=20,
            pady=15,
            relief="flat"
        )
        
        scrollbar = ttk.Scrollbar(text_scroll_frame, orient="vertical", command=self.text_display.yview)
        self.text_display.configure(yscrollcommand=scrollbar.set)
        
        self.text_display.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure text tags with modern colors
        self.text_display.tag_configure("correct", background=self.colors['success'], foreground="white", relief="flat")
        self.text_display.tag_configure("incorrect", background=self.colors['error'], foreground="white", relief="flat")
        self.text_display.tag_configure("current", background=self.colors['accent'], foreground="white", relief="flat")
        
        # Input section with modern styling
        input_card = tk.Frame(main_container, bg=self.colors['bg_secondary'])
        input_card.pack(fill="x", pady=(0, 20))
        
        input_border = tk.Frame(input_card, bg=self.colors['accent'], height=3)
        input_border.pack(fill="x")
        
        input_content = tk.Frame(input_card, bg=self.colors['bg_secondary'])
        input_content.pack(fill="x", padx=20, pady=15)
        
        tk.Label(
            input_content,
            text="⌨️ Type here:",
            font=self.heading_font,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(anchor="w", pady=(0, 10))
        
        self.input_entry = tk.Entry(
            input_content,
            font=self.mono_font,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            state="disabled",
            insertbackground=self.colors['accent'],
            selectbackground=self.colors['accent'],
            border=0,
            relief="flat"
        )
        self.input_entry.pack(fill="x", ipady=12)
        self.input_entry.bind('<KeyRelease>', self.on_key_press)
        
        # Stats section with cards
        stats_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        stats_frame.pack(fill="x")
        
        # Create individual stat cards
        self.create_stat_card(stats_frame, "⚡", "WPM", "0", self.colors['info'], "wpm")
        self.create_stat_card(stats_frame, "🎯", "Accuracy", "0%", self.colors['success'], "accuracy")
        self.create_stat_card(stats_frame, "📊", "Progress", "0%", self.colors['warning'], "progress")
    
    def create_stat_card(self, parent, icon, title, value, color, stat_type):
        """Create a modern stat card"""
        card = tk.Frame(parent, bg=self.colors['bg_secondary'], relief="flat")
        card.pack(side="left", fill="x", expand=True, padx=5)
        
        # Color border
        border = tk.Frame(card, bg=color, height=3)
        border.pack(fill="x")
        
        content = tk.Frame(card, bg=self.colors['bg_secondary'])
        content.pack(fill="x", padx=15, pady=15)
        
        # Icon and title
        header = tk.Frame(content, bg=self.colors['bg_secondary'])
        header.pack(fill="x")
        
        tk.Label(
            header,
            text=f"{icon} {title}",
            font=self.body_font,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack(side="left")
        
        # Value
        value_label = tk.Label(
            content,
            text=value,
            font=font.Font(family="Arial", size=18, weight="bold"),
            bg=self.colors['bg_secondary'],
            fg=color
        )
        value_label.pack(pady=(5, 0))
        
        # Store reference for updating
        if stat_type == "wpm":
            self.wpm_label = value_label
        elif stat_type == "accuracy":
            self.accuracy_label = value_label
        elif stat_type == "progress":
            self.progress_label = value_label
        
    def generate_text(self):
        """Generate random text based on difficulty level"""
        difficulty = self.difficulty_var.get()
        words = self.word_lists[difficulty]
        
        # Generate 50-80 words for the test
        num_words = random.randint(50, 80)
        selected_words = [random.choice(words) for _ in range(num_words)]
        
        return " ".join(selected_words)
    
    def start_game(self):
        """Start the typing speed game"""
        # Set time limit
        time_setting = self.time_var.get()
        self.time_limit = 120 if "2" in time_setting else 180
        self.remaining_time = self.time_limit
        
        # Generate text
        self.current_text = self.generate_text()
        
        # Reset variables
        self.current_position = 0
        self.correct_chars = 0
        self.total_chars = 0
        self.start_time = time.time()
        
        # Update UI
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, "end")
        self.text_display.insert(1.0, self.current_text)
        self.text_display.config(state="disabled")
        
        self.input_entry.config(state="normal")
        self.input_entry.delete(0, "end")
        self.input_entry.focus()
        
        self.start_button.config(state="disabled", text="🎮 Game in Progress...", bg=self.colors['text_secondary'])
        
        # Start timer
        self.timer_running = True
        self.start_timer()
        
        # Update display
        self.update_display()
    
    def start_timer(self):
        """Start the countdown timer"""
        def countdown():
            while self.timer_running and self.remaining_time > 0:
                minutes = self.remaining_time // 60
                seconds = self.remaining_time % 60
                self.timer_label.config(text=f"⏰ Time: {minutes}:{seconds:02d}")
                time.sleep(1)
                self.remaining_time -= 1
            
            if self.remaining_time <= 0:
                self.end_game()
        
        timer_thread = threading.Thread(target=countdown, daemon=True)
        timer_thread.start()
    
    def on_key_press(self, event):
        """Handle key press events"""
        if not self.timer_running:
            return
            
        typed_text = self.input_entry.get()
        self.current_position = len(typed_text)
        
        # Check if game is complete
        if self.current_position >= len(self.current_text):
            self.end_game()
            return
        
        # Calculate accuracy
        self.total_chars = self.current_position
        self.correct_chars = 0
        
        for i in range(min(len(typed_text), len(self.current_text))):
            if typed_text[i] == self.current_text[i]:
                self.correct_chars += 1
        
        self.update_display()
        self.highlight_text(typed_text)
    
    def highlight_text(self, typed_text):
        """Highlight correct/incorrect characters"""
        self.text_display.config(state="normal")
        
        # Remove all tags
        self.text_display.tag_remove("correct", 1.0, "end")
        self.text_display.tag_remove("incorrect", 1.0, "end")
        self.text_display.tag_remove("current", 1.0, "end")
        
        # Highlight typed characters
        for i in range(len(typed_text)):
            start_pos = f"1.{i}"
            end_pos = f"1.{i+1}"
            
            if i < len(self.current_text):
                if typed_text[i] == self.current_text[i]:
                    self.text_display.tag_add("correct", start_pos, end_pos)
                else:
                    self.text_display.tag_add("incorrect", start_pos, end_pos)
        
        # Highlight current character
        if len(typed_text) < len(self.current_text):
            current_pos = f"1.{len(typed_text)}"
            next_pos = f"1.{len(typed_text)+1}"
            self.text_display.tag_add("current", current_pos, next_pos)
        
        self.text_display.config(state="disabled")
    
    def update_display(self):
        """Update WPM, accuracy, and progress displays"""
        if self.start_time:
            # Calculate WPM
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 0:
                words_typed = self.correct_chars / 5  # Average word length
                wpm = int((words_typed / elapsed_time) * 60)
                self.wpm_label.config(text=f"{wpm}")
            
            # Calculate accuracy
            if self.total_chars > 0:
                accuracy = int((self.correct_chars / self.total_chars) * 100)
                self.accuracy_label.config(text=f"{accuracy}%")
            
            # Calculate progress
            progress = int((self.current_position / len(self.current_text)) * 100)
            self.progress_label.config(text=f"{progress}%")
    
    def end_game(self):
        """End the game and show results"""
        self.timer_running = False
        self.end_time = time.time()
        
        # Disable input
        self.input_entry.config(state="disabled")
        self.start_button.config(state="normal", text="🚀 Start Game", bg=self.colors['accent'])
        
        # Calculate final stats
        elapsed_time = self.end_time - self.start_time
        words_typed = self.correct_chars / 5
        final_wpm = int((words_typed / elapsed_time) * 60) if elapsed_time > 0 else 0
        final_accuracy = int((self.correct_chars / self.total_chars) * 100) if self.total_chars > 0 else 0
        
        # Show beautiful results dialog
        self.show_results_dialog(final_wpm, final_accuracy, elapsed_time)
    
    def show_results_dialog(self, wpm, accuracy, elapsed_time):
        """Show a beautiful results dialog"""
        # Create custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("🏆 Game Results")
        dialog.geometry("450x500")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.colors['accent'], height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🏆 Game Complete!",
            font=font.Font(family="Arial", size=20, weight="bold"),
            bg=self.colors['accent'],
            fg="white"
        ).pack(expand=True)
        
        # Content
        content_frame = tk.Frame(dialog, bg=self.colors['bg_primary'])
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Performance rating
        rating = self.get_performance_rating(wpm, accuracy)
        rating_parts = rating.split(' ', 1)
        emoji = rating_parts[0] if len(rating_parts) > 1 else "📚"
        text = rating_parts[1] if len(rating_parts) > 1 else rating
        
        tk.Label(
            content_frame,
            text=emoji,
            font=font.Font(size=40),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent']
        ).pack(pady=(0, 10))
        
        tk.Label(
            content_frame,
            text=text,
            font=font.Font(family="Arial", size=14, weight="bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            wraplength=350,
            justify="center"
        ).pack(pady=(0, 30))
        
        # Stats cards
        stats = [
            ("⚡", "Words Per Minute", f"{wpm}", self.colors['info']),
            ("🎯", "Accuracy", f"{accuracy}%", self.colors['success']),
            ("⏱️", "Time Taken", f"{elapsed_time:.1f}s", self.colors['warning']),
            ("📝", "Difficulty", self.difficulty_var.get(), self.colors['accent'])
        ]
        
        for icon, label, value, color in stats:
            card = tk.Frame(content_frame, bg=self.colors['bg_secondary'])
            card.pack(fill="x", pady=5)
            
            border = tk.Frame(card, bg=color, height=2)
            border.pack(fill="x")
            
            card_content = tk.Frame(card, bg=self.colors['bg_secondary'])
            card_content.pack(fill="x", padx=15, pady=10)
            
            tk.Label(
                card_content,
                text=f"{icon} {label}",
                font=self.body_font,
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            ).pack(side="left")
            
            tk.Label(
                card_content,
                text=value,
                font=font.Font(family="Arial", size=14, weight="bold"),
                bg=self.colors['bg_secondary'],
                fg=color
            ).pack(side="right")
        
        # Close button
        tk.Button(
            content_frame,
            text="✨ Awesome!",
            font=self.heading_font,
            bg=self.colors['accent'],
            fg="white",
            command=dialog.destroy,
            padx=30,
            pady=10,
            border=0,
            cursor="hand2",
            activebackground=self.colors['accent_hover'],
            relief="flat"
        ).pack(pady=(30, 0))
    
    def get_performance_rating(self, wpm, accuracy):
        """Get performance rating based on WPM and accuracy"""
        if wpm >= 60 and accuracy >= 95:
            return "🏆 Excellent! Professional level typing!"
        elif wpm >= 40 and accuracy >= 90:
            return "🥇 Great! Above average typing skills!"
        elif wpm >= 25 and accuracy >= 80:
            return "🥈 Good! Average typing skills!"
        elif wpm >= 15 and accuracy >= 70:
            return "🥉 Fair! Keep practicing!"
        else:
            return "📚 Beginner! Practice more to improve!"

def main():
    root = tk.Tk()
    game = TypingSpeedGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()