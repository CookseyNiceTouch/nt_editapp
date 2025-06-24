#!/usr/bin/env python3
"""
FastAPI Asset Analysis Test UI

A simple customtkinter interface for testing video analysis API endpoints.
Features:
- Drag and drop video file selection
- Click to browse file selection
- Submit analysis jobs to FastAPI server
- Real-time status monitoring
- Job results display
"""

import os
import sys
import json
import requests
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Configure customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VideoAnalysisTestUI:
    """Main UI class for testing video analysis API"""
    
    def __init__(self):
        # API configuration
        self.api_base_url = "http://localhost:8000"
        self.current_job_id: Optional[str] = None
        self.status_update_thread: Optional[threading.Thread] = None
        self.stop_status_updates = False
        
        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        # Configure main window
        self.root = TkinterDnD.Tk()
        self.root.title("Video Analysis Test UI")
        self.root.geometry("600x500")  # Reduced height since removing results pane
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Setup sections
        self.setup_api_status_section()
        self.setup_file_selection_section()
        self.setup_analysis_controls_section()
        self.setup_status_display_section()
        # Removed results section
        
        # Setup drag and drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_file_drop)
        
        # Start API status checking
        self.check_api_status()
        self.root.after(5000, self.periodic_api_check)
        
    def setup_api_status_section(self):
        """Setup API connection status display"""
        api_frame = ctk.CTkFrame(self.main_frame)
        api_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        api_frame.grid_columnconfigure(1, weight=1)
        
        # API Status
        ctk.CTkLabel(api_frame, text="API Status:", font=ctk.CTkFont(size=12, weight="bold")).grid(
            row=0, column=0, padx=(10, 5), pady=8, sticky="w"
        )
        
        self.api_status_label = ctk.CTkLabel(
            api_frame, 
            text="Checking...", 
            font=ctk.CTkFont(size=11),
            text_color="orange"
        )
        self.api_status_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        
        self.refresh_api_btn = ctk.CTkButton(
            api_frame,
            text="Refresh",
            width=60,
            height=24,
            font=ctk.CTkFont(size=11),
            command=self.check_api_status
        )
        self.refresh_api_btn.grid(row=0, column=2, padx=8, pady=6)
        
    def setup_file_selection_section(self):
        """Setup file selection with inline browse button"""
        file_frame = ctk.CTkFrame(self.main_frame)
        file_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        file_frame.grid_columnconfigure(1, weight=1)  # Make file path column expandable
        
        # Section title
        ctk.CTkLabel(
            file_frame, 
            text="File Selection", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(8, 5))
        
        # File path display and browse button on same row
        ctk.CTkLabel(
            file_frame, 
            text="File:"
        ).grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.file_path_label = ctk.CTkLabel(
            file_frame,
            text="No file selected (drag & drop or browse)",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.file_path_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse",
            width=80,
            height=28,
            command=self.browse_file
        )
        self.browse_btn.grid(row=1, column=2, padx=(5, 10), pady=5)
        
        # Drag & drop instruction
        ctk.CTkLabel(
            file_frame,
            text="💡 Tip: You can also drag & drop video files directly onto this window",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).grid(row=2, column=0, columnspan=3, pady=(0, 8))
        
    def setup_analysis_controls_section(self):
        """Setup analysis controls with inline button"""
        controls_frame = ctk.CTkFrame(self.main_frame)
        controls_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        controls_frame.grid_columnconfigure(1, weight=1)  # Make input column expandable
        
        # Section title
        ctk.CTkLabel(
            controls_frame, 
            text="Analysis Settings", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(8, 5))
        
        # Silence threshold setting and submit button on same row
        ctk.CTkLabel(
            controls_frame, 
            text="Silence Threshold (ms):"
        ).grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.silence_threshold_var = tk.StringVar(value="1000")
        silence_entry = ctk.CTkEntry(
            controls_frame,
            textvariable=self.silence_threshold_var,
            width=100,
            height=32
        )
        silence_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.submit_btn = ctk.CTkButton(
            controls_frame,
            text="Start Analysis",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=32,
            width=120,
            command=self.submit_analysis,
            state="disabled"
        )
        self.submit_btn.grid(row=1, column=2, padx=(5, 10), pady=5)
        
    def setup_status_display_section(self):
        """Setup status display with copy functionality"""
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Title and copy button row
        title_frame = ctk.CTkFrame(status_frame)
        title_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 0))
        title_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            title_frame, 
            text="Status & Progress", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.copy_btn = ctk.CTkButton(
            title_frame,
            text="📋 Copy",
            width=70,
            height=24,
            font=ctk.CTkFont(size=10),
            command=self.copy_status_to_clipboard
        )
        self.copy_btn.grid(row=0, column=1, padx=(5, 0), pady=5)
        
        # Status display - much taller for better readability
        self.status_text = ctk.CTkTextbox(
            status_frame,
            height=200,  # Increased from 100 to 200
            font=ctk.CTkFont(family="Consolas", size=10),
            wrap="word"
        )
        self.status_text.grid(row=1, column=0, sticky="ew", padx=8, pady=(5, 8))
        
        # Initialize with ready message
        self.update_status_display("Ready to analyze video files...")
    
    def copy_status_to_clipboard(self):
        """Copy status text content to clipboard for debugging"""
        try:
            status_content = self.status_text.get("1.0", tk.END).strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(status_content)
            
            # Temporarily change button text to show success
            original_text = self.copy_btn.cget("text")
            self.copy_btn.configure(text="✅ Copied!")
            self.root.after(1500, lambda: self.copy_btn.configure(text=original_text))
            
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")
    
    def periodic_api_check(self):
        """Periodically check API status"""
        self.check_api_status()
        self.root.after(5000, self.periodic_api_check)  # Check every 5 seconds
    
    def check_api_status(self):
        """Check if the FastAPI server is running"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=3)
            if response.status_code == 200:
                self.api_status_label.configure(text="Connected ✓", text_color="green")
                return True
            else:
                self.api_status_label.configure(text="API Error", text_color="red")
                return False
        except requests.exceptions.RequestException:
            self.api_status_label.configure(text="Disconnected ✗", text_color="red")
            return False
    
    def on_file_drop(self, event):
        """Handle drag and drop file selection"""
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]
            self.select_file(file_path)
    
    def browse_file(self):
        """Handle browse button file selection"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.mov *.avi *.mkv *.wmv *.flv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.select_file(file_path)
    
    def select_file(self, file_path: str):
        """Process selected file"""
        if os.path.isfile(file_path):
            self.file_path_label.configure(text=f"Selected: {os.path.basename(file_path)}")
            self.selected_file_path = file_path
            self.submit_btn.configure(state="normal")
            self.update_status_display(f"File selected: {file_path}")
        else:
            messagebox.showerror("Error", "Selected file does not exist!")
    
    def submit_analysis(self):
        """Submit video for analysis"""
        if not hasattr(self, 'selected_file_path'):
            messagebox.showerror("Error", "Please select a video file first!")
            return
        
        if not self.check_api_status():
            messagebox.showerror("Error", "API server is not available!")
            return
        
        try:
            # Prepare request data
            request_data = {
                "video_path": self.selected_file_path,
                "silence_threshold_ms": int(self.silence_threshold_var.get())
            }
            
            # Submit analysis job
            self.update_status_display("Submitting analysis job...")
            response = requests.post(
                f"{self.api_base_url}/analysis/start",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.current_job_id = result["job_id"]
                
                self.update_status_display(
                    f"Analysis job submitted successfully!\n"
                    f"Job ID: {self.current_job_id}\n"
                    f"Status: {result['status']}\n"
                    f"Starting status monitoring..."
                )
                
                # Start status monitoring
                self.start_status_monitoring()
                
                # Disable submit button
                self.submit_btn.configure(state="disabled")
                
            else:
                error_msg = f"Failed to submit job: {response.status_code}"
                if response.headers.get('content-type', '').startswith('application/json'):
                    error_data = response.json()
                    error_msg += f"\n{error_data.get('detail', 'Unknown error')}"
                
                self.update_status_display(error_msg)
                messagebox.showerror("Submission Error", error_msg)
        
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid silence threshold: {e}")
        except Exception as e:
            error_msg = f"Error submitting analysis: {str(e)}"
            self.update_status_display(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def start_status_monitoring(self):
        """Start background thread to monitor job status"""
        if self.status_update_thread and self.status_update_thread.is_alive():
            self.stop_status_updates = True
            self.status_update_thread.join()
        
        self.stop_status_updates = False
        self.status_update_thread = threading.Thread(target=self.monitor_job_status)
        self.status_update_thread.daemon = True
        self.status_update_thread.start()
    
    def monitor_job_status(self):
        """Background thread function to monitor job status"""
        while not self.stop_status_updates and self.current_job_id:
            try:
                response = requests.get(
                    f"{self.api_base_url}/analysis/status/{self.current_job_id}",
                    timeout=10
                )
                
                if response.status_code == 200:
                    status_data = response.json()
                    
                    # Update UI in main thread
                    self.root.after(0, self.update_job_status_display, status_data)
                    
                    # Check if job is complete
                    if status_data["status"] in ["completed", "failed"]:
                        self.root.after(0, self.on_job_complete, status_data)
                        break
                
                else:
                    error_msg = f"Failed to get status: {response.status_code}"
                    self.root.after(0, self.update_status_display, error_msg)
                
            except Exception as e:
                error_msg = f"Status check error: {str(e)}"
                self.root.after(0, self.update_status_display, error_msg)
            
            # Wait before next check
            time.sleep(3)
    
    def update_job_status_display(self, status_data: Dict[str, Any]):
        """Update the status display with job information"""
        status = status_data["status"].upper()
        message = status_data.get("message", "")
        progress = status_data.get("progress", "")
        
        # Format the display
        display_text = f"Job ID: {status_data['job_id']}\n"
        display_text += f"Status: {status}\n"
        display_text += f"Message: {message}\n"
        
        if progress and progress != message:
            display_text += f"Progress: {progress}\n"
        
        display_text += f"Created: {status_data['created_at']}\n"
        
        if status_data.get("completed_at"):
            display_text += f"Completed: {status_data['completed_at']}\n"
        
        if status_data.get("error"):
            display_text += f"Error: {status_data['error']}\n"
        
        self.update_status_display(display_text)
    
    def on_job_complete(self, status_data: Dict[str, Any]):
        """Handle job completion"""
        self.stop_status_updates = True
        
        if status_data["status"] == "completed":
            self.update_status_display(
                f"✅ Analysis completed successfully!\n"
                f"Output file: {status_data.get('output_file', 'N/A')}"
            )
        
        elif status_data["status"] == "failed":
            error_msg = status_data.get('error', 'Unknown error')
            self.update_status_display(f"❌ Analysis failed: {error_msg}")
        
        # Re-enable submit button
        self.submit_btn.configure(state="normal")
        self.current_job_id = None
    
    def update_status_display(self, message: str):
        """Update the status text display"""
        timestamp = time.strftime("%H:%M:%S")
        status_message = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, status_message)
        self.status_text.see(tk.END)
    
    def run(self):
        """Start the UI application"""
        try:
            self.root.mainloop()
        finally:
            # Clean up
            self.stop_status_updates = True
            if self.status_update_thread and self.status_update_thread.is_alive():
                self.status_update_thread.join(timeout=1)

def main():
    """Main entry point"""
    print("Starting Video Analysis Test UI...")
    
    # Check if required packages are available
    try:
        import customtkinter
        import tkinterdnd2
        import requests
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install required packages:")
        print("  uv add customtkinter tkinterdnd2 requests")
        return
    
    # Start the UI
    app = VideoAnalysisTestUI()
    app.run()

if __name__ == "__main__":
    main()
