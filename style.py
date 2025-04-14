import tkinter as tk
from tkinter import ttk

class StyleManager:
    def __init__(self):
        self.style = ttk.Style()
        self.setup_themes()
        
    def setup_themes(self):
        # Modern color palette
        self.colors = {
            "primary": "#4a6fa5",
            "secondary": "#166088", 
            "accent": "#4fc3f7",
            "background": "#f5f7fa",
            "text": "#333333",
            "light_text": "#ffffff",
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336",
            "border": "#d1d5db",
            "highlight": "#ffcc00",  # Highlight color for active elements
            "info": "#2196F3",       # Info color for informational messages
            "danger": "#f44336",     # Danger color for error messages
            "success": "#4caf50",    # Success color for success messages
            "warning": "#ff9800"     # Warning color for alerts
        }
        
        # Configure root style
        self.style.configure('.', 
            background=self.colors["background"],
            foreground=self.colors["text"],
            font=('Segoe UI', 10),
            padding=5
        )
        
        # Button styles with rounded corners and better hover effects
        self.style.configure('TButton',
            padding=8,
            relief='flat',
            font=('Segoe UI', 10, 'bold'),
            background=self.colors["primary"],
            foreground=self.colors["light_text"],
            borderwidth=0,
            focusthickness=3,
            focuscolor='none',
            bordercolor=self.colors["border"],
            borderradius=6
        )
        self.style.map('TButton',
            background=[
                ('active', self.colors["secondary"]),
                ('pressed', self.colors["secondary"]),
                ('disabled', '#cccccc')
            ],
            foreground=[
                ('active', self.colors["light_text"]),
                ('disabled', '#888888')
            ],
            lightcolor=[('pressed', self.colors["secondary"])],
            darkcolor=[('pressed', self.colors["secondary"])]
        )
        
        # Accent button style
        self.style.configure('Accent.TButton',
            background=self.colors["accent"],
            foreground=self.colors["light_text"],
            borderradius=6
        )
        self.style.map('Accent.TButton',
            background=[('active', '#3aa8d8')]
        )
        
        # Entry styles with better focus indication
        self.style.configure('TEntry',
            padding=8,
            relief='solid',
            bordercolor=self.colors["border"],
            lightcolor=self.colors["background"],
            darkcolor=self.colors["border"],
            fieldbackground=self.colors["background"],
            insertcolor=self.colors["text"],
            focuscolor=self.colors["accent"] + '40',  # 25% opacity
            borderwidth=1,
            bordercursor='xterm'
        )
        self.style.map('TEntry',
            bordercolor=[
                ('focus', self.colors["accent"]),
                ('hover', self.colors["primary"])
            ],
            lightcolor=[('focus', self.colors["accent"] + '20')]
        )
        
        # Combobox styles with dropdown improvements
        self.style.configure('TCombobox',
            padding=8,
            relief='solid',
            bordercolor=self.colors["border"],
            background=self.colors["background"],
            arrowcolor=self.colors["primary"],
            arrowsize=12,
            borderwidth=1
        )
        self.style.map('TCombobox',
            bordercolor=[
                ('focus', self.colors["accent"]),
                ('hover', self.colors["primary"])
            ],
            arrowcolor=[
                ('active', self.colors["secondary"]),
                ('pressed', self.colors["secondary"])
            ]
        )
        
        # Label styles with better typography
        self.style.configure('TLabel',
            padding=6,
            font=('Segoe UI', 10),
            background=self.colors["background"]
        )
        self.style.configure('Header.TLabel',
            font=('Segoe UI', 12, 'bold'),
            padding=(0, 10, 0, 5)
        )
        
        # Frame styles with subtle borders
        self.style.configure('TFrame',
            background=self.colors["background"],
            relief='flat',
            borderwidth=0
        )
        self.style.configure('Border.TFrame',
            background=self.colors["background"],
            relief='flat',
            borderwidth=1,
            bordercolor=self.colors["border"]
        )
        
        # Scrollbar styles with modern look
        self.style.configure('Vertical.TScrollbar',
            gripcount=0,
            background=self.colors["primary"] + '80',  # 50% opacity
            troughcolor=self.colors["background"],
            bordercolor=self.colors["background"],
            arrowcolor=self.colors["light_text"],
            arrowsize=14,
            width=12
        )
        self.style.map('Vertical.TScrollbar',
            background=[
                ('active', self.colors["primary"]),
                ('pressed', self.colors["secondary"])
            ]
        )
        
        # Notebook styles with better tab appearance
        self.style.configure('TNotebook',
            tabmargins=[2, 5, 2, 0],
            background=self.colors["background"],
            bordercolor=self.colors["border"]
        )
        self.style.configure('TNotebook.Tab',
            padding=[12, 6],
            background=self.colors["background"],
            foreground=self.colors["text"],
            borderwidth=1,
            bordercolor=self.colors["border"],
            focuscolor=self.colors["background"]
        )
        self.style.map('TNotebook.Tab',
            background=[
                ('selected', self.colors["background"]),
                ('active', self.colors["primary"] + '20')
            ],
            bordercolor=[
                ('selected', self.colors["border"]),
                ('active', self.colors["primary"])
            ],
            lightcolor=[('selected', self.colors["background"])]
        )
        
    def get_colors(self):
        return self.colors
        
    def apply_theme(self, root):
        root.configure(bg=self.colors["background"])
        self.style.theme_use('clam')  # Use a modern theme as base
