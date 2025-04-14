import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from style import StyleManager
import speech_recognition as sr
import threading
from datetime import datetime
import json
import re
import webbrowser
from main import SearchAssistant

class EnhancedSearchAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.assistant = SearchAssistant()
        self.style_manager = StyleManager()
        self.colors = self.style_manager.get_colors()
        self.style_manager.apply_theme(root)
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Virtual Search Assistant")
        self.root.geometry("1000x700")
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["background"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search Frame
        self.search_frame = tk.Frame(main_frame)
        self.search_frame.pack(fill=tk.X, pady=10)
        
        # Search Entry with suggestions
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Combobox(
            self.search_frame,
            textvariable=self.search_var,
            width=60,
            font=('Segoe UI', 12)
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.update_suggestions)
        self.search_entry.bind('<Return>', self.handle_search)
        
        # Search Button
        search_btn = ttk.Button(
            self.search_frame,
            text="Search",
            command=self.handle_search,
            style='Accent.TButton'
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # History Button
        history_btn = ttk.Button(
            self.search_frame,
            text="History",
            command=self.show_history
        )
        history_btn.pack(side=tk.LEFT, padx=5)
        
        # Analytics Button
        analytics_btn = ttk.Button(
            self.search_frame,
            text="Analytics",
            command=self.show_analytics
        )
        analytics_btn.pack(side=tk.LEFT, padx=5)

        # Voice Search Button
        voice_btn = ttk.Button(
            self.search_frame,
            text="🎤 Voice",
            command=self.start_voice_search,
            style='Accent.TButton'
        )
        voice_btn.pack(side=tk.LEFT, padx=5)
        
        # Filter Controls Frame
        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        # Search Type Filter (removed image/video options)
        tk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value='All')
        ttk.OptionMenu(
            filter_frame,
            self.filter_var,
            'All',
            'All'
        ).pack(side=tk.LEFT, padx=5)
        
        # Date Filter
        tk.Label(filter_frame, text="Date:").pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value='Any time')
        ttk.OptionMenu(
            filter_frame,
            self.date_var,
            'Any time',
            'Any time',
            'Past 24h',
            'Past week',
            'Past month',
            'Past year'
        ).pack(side=tk.LEFT, padx=5)
        
        
        # Results Display
        self.results_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=100,
            height=30,
            font=('Segoe UI', 11),
            bg=self.colors["background"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief='flat',
            borderwidth=2
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.configure(state='disabled')
        
        
        
    def update_suggestions(self, event):
        """Update search suggestions as user types"""
        query = self.search_var.get()
        if len(query) > 2:  # Only fetch suggestions after 3 characters
            suggestions = self.assistant.get_suggestions(query)
            self.search_entry['values'] = suggestions

    def handle_search(self, event=None):
        query = self.search_var.get()
        if query:
            self.display_result(f"🔎 Searching: {query}\n", "query")
            
            # Get filter values
            filter_type = None
            if self.filter_var.get() != 'All':
                filter_type = self.filter_var.get().lower()
                
            date_range = None
            date_map = {
                'Past 24h': 'd1',
                'Past week': 'd7',
                'Past month': 'd30',
                'Past year': 'd365'
            }
            if self.date_var.get() != 'Any time':
                date_range = date_map[self.date_var.get()]
                
            site_filter = None
            
            response = self.assistant.generate_response(
                query,
                filter_type=filter_type,
                date_range=date_range,
                site_filter=site_filter
            )
            
            self.display_result(f"{response}\n\n")
                
            self.search_entry.delete(0, tk.END)

            
    def show_history(self):
        """Show enhanced history with search and sort options"""
        # Create a new top-level window for history if it doesn't exist
        if not hasattr(self, 'history_window') or not self.history_window.winfo_exists():
            self.history_window = tk.Toplevel(self.root)
            self.history_window.title("Search History")
            self.history_window.geometry("600x400")
            
            # Initialize history variables
            self.history_search_var = tk.StringVar()
            self.sort_var = tk.StringVar(value='recent')
            
            # Create history control frame
            control_frame = tk.Frame(self.history_window)
            control_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Search history entry
            tk.Label(control_frame, text="Search History:").pack(side=tk.LEFT, padx=5)
            history_search = ttk.Entry(control_frame, textvariable=self.history_search_var, width=30)
            history_search.pack(side=tk.LEFT, padx=5)
            history_search.bind('<Return>', lambda e: self.refresh_history())
            
            # Sort options
            tk.Radiobutton(
                control_frame, 
                text="Recent", 
                variable=self.sort_var, 
                value='recent',
                command=self.refresh_history
            ).pack(side=tk.LEFT, padx=5)
            tk.Radiobutton(
                control_frame, 
                text="Frequent", 
                variable=self.sort_var, 
                value='frequent',
                command=self.refresh_history
            ).pack(side=tk.LEFT, padx=5)
            
            # History display frame
            self.history_frame = tk.Frame(self.history_window)
            self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Close button
            close_btn = tk.Button(
                self.history_window,
                text="Close",
                command=self.history_window.destroy
            )
            close_btn.pack(side=tk.BOTTOM, pady=5)
            
            self.refresh_history()
        else:
            # Bring existing window to front
            self.history_window.lift()
        
    def refresh_history(self):
        """Refresh history display with current filters"""
        # Clear previous history display
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        # Get filtered and sorted history
        search_term = self.history_search_var.get()
        sort_by = self.sort_var.get()
        history_text = self.assistant.get_history(search_term, sort_by)
        
        if history_text.startswith("No"):
            tk.Label(
                self.history_frame,
                text=history_text,
                font=('Segoe UI', 10)
            ).pack()
            return
            
        # Display each history item with delete button
        history_items = history_text.split('\n')
        for i, item in enumerate(history_items):
            item_frame = tk.Frame(self.history_frame)
            item_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                item_frame,
                text=item,
                font=('Segoe UI', 10),
                anchor='w'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Button(
                item_frame,
                text="🗑️",
                command=lambda idx=i: self.delete_single_item(idx),
                font=('Segoe UI', 10),
                relief=tk.FLAT
            ).pack(side=tk.RIGHT)
        
    def delete_single_item(self, index):
        """Delete a single history item by index"""
        result = self.assistant.delete_history_item(index)
        self.display_result(f"\n{result}\n", "query")
        self.show_history()  # Refresh the history display
        
    def show_analytics(self):
        """Display search analytics dashboard"""
        self.display_result("\n📊 Loading analytics...\n", "query")
        analytics = self.assistant.get_analytics()
        self.display_result(f"{analytics}\n\n")

    def export_history(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump({
                        "history": self.assistant.search_history,
                        "timestamp": str(datetime.now())
                    }, f, indent=2)
                messagebox.showinfo("Success", "History exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
            
    def delete_history(self):
        """Handle history deletion with confirmation"""
        if not self.assistant.search_history:
            messagebox.showinfo("Info", "History is already empty")
            return
            
        if messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete all search history?",
            icon='warning'
        ):
            result = self.assistant.clear_history()
            self.display_result(f"\n{result}\n", "query")
            
    def start_voice_search(self):
        """Start voice recognition in a separate thread"""
        def recognize_thread():
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    self.display_result("\n🎤 Listening... Speak now\n", "query")
                    audio = r.listen(source, timeout=5)
                    try:
                        text = r.recognize_google(audio)
                        self.search_var.set(text)
                        self.display_result(f"🎤 Heard: {text}\n", "query")
                        self.handle_search()
                    except sr.UnknownValueError:
                        self.display_result("🎤 Could not understand audio\n", "query")
                    except sr.RequestError as e:
                        self.display_result(f"🎤 Error: {str(e)}\n", "query")
                    except Exception as e:
                        self.display_result(f"🎤 Error: {str(e)}\n", "query")
            except Exception as e:
                self.display_result(f"🎤 Error: {str(e)}\n", "query")

        # Start recognition in a separate thread to avoid freezing the GUI
        threading.Thread(target=recognize_thread, daemon=True).start()

    def display_result(self, text, tag=None):
        self.results_text.config(state=tk.NORMAL)
        
        # Find all URLs in the text
        url_pattern = re.compile(r'https?://\S+')
        urls = url_pattern.finditer(text)
        
        # Insert text with URL highlighting
        last_pos = 0
        for match in urls:
            # Insert text before URL
            self.results_text.insert(tk.END, text[last_pos:match.start()], tag)
            # Insert URL with clickable tag
            url = match.group()
            self.results_text.insert(tk.END, url, ('link', tag))
            last_pos = match.end()
        
        # Insert remaining text
        self.results_text.insert(tk.END, text[last_pos:], tag)
        
        # Configure link appearance and behavior
        self.results_text.tag_config('link', foreground='blue', underline=1)
        self.results_text.tag_bind('link', '<Button-1>', self.open_link)
        
        self.results_text.config(state=tk.DISABLED)
        self.results_text.see(tk.END)
        
    def open_link(self, event):
        """Open clicked URL in default browser"""
        index = self.results_text.index(f"@{event.x},{event.y}")
        tags = self.results_text.tag_names(index)
        
        if 'link' in tags:
            # Get the URL text
            start = f"{index} linestart"
            end = f"{index} lineend"
            line = self.results_text.get(start, end)
            
            # Find URL in line (in case multiple links on same line)
            url_pattern = re.compile(r'https?://\S+')
            urls = url_pattern.finditer(line)
            for url in urls:
                if self.results_text.compare(index, '>=', f"{start}+{url.start()}c") and \
                   self.results_text.compare(index, '<=', f"{start}+{url.end()}c"):
                    webbrowser.open_new(url.group())
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedSearchAssistantGUI(root)
    root.mainloop()
