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
        """Initialize the main UI components"""
        # Create main window with drag-and-drop support
        self.root = TkinterDnD.Tk()
        self.root.title("Video Analysis API Test")
        self.root.geometry("800x700")
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Video Analysis API Test",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30))
        
        # API Status
        self.setup_api_status_section()
        
        # File Selection Section
        self.setup_file_selection_section()
        
        # Analysis Controls
        self.setup_analysis_controls_section()
        
        # Status Display
        self.setup_status_display_section()
        
        # Results Display
        self.setup_results_section()
        
        # Check API status on startup
        self.check_api_status()
        
    def setup_api_status_section(self):
        """Setup API connection status display"""
        api_frame = ctk.CTkFrame(self.main_frame)
        api_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        api_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(api_frame, text="API Status:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.api_status_label = ctk.CTkLabel(
            api_frame, 
            text="Checking...", 
            text_color="orange"
        )
        self.api_status_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.refresh_api_btn = ctk.CTkButton(
            api_frame,
            text="Refresh",
            width=80,
            command=self.check_api_status
        )
        self.refresh_api_btn.grid(row=0, column=2, padx=10, pady=10)
        
    def setup_file_selection_section(self):
        """Setup drag-and-drop and file selection area"""
        file_frame = ctk.CTkFrame(self.main_frame)
        file_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        file_frame.grid_columnconfigure(0, weight=1)
        
        # Section title
        ctk.CTkLabel(
            file_frame, 
            text="Select Video File", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10))
        
        # Drag and drop area
        self.drop_frame = ctk.CTkFrame(file_frame, height=120)
        self.drop_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.drop_frame.grid_columnconfigure(0, weight=1)
        self.drop_frame.grid_propagate(False)
        
        # Configure drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_file_drop)
        
        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="Drag & Drop Video File Here\nor Click Browse Below",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.drop_label.grid(row=0, column=0, pady=40)
        
        # Browse button
        self.browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse for Video File",
            command=self.browse_file
        )
        self.browse_btn.grid(row=2, column=0, pady=(0, 10))
        
        # Selected file display
        self.file_path_var = tk.StringVar()
        self.file_path_label = ctk.CTkLabel(
            file_frame,
            textvariable=self.file_path_var,
            font=ctk.CTkFont(size=10),
            text_color="green"
        )
        self.file_path_label.grid(row=3, column=0, pady=(0, 15), padx=20, sticky="ew")
        
    def setup_analysis_controls_section(self):
        """Setup analysis submission controls"""
        controls_frame = ctk.CTkFrame(self.main_frame)
        controls_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Section title
        ctk.CTkLabel(
            controls_frame, 
            text="Analysis Settings", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10))
        
        # Settings frame
        settings_frame = ctk.CTkFrame(controls_frame)
        settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Silence threshold
        ctk.CTkLabel(settings_frame, text="Silence Threshold (ms):").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.silence_threshold_var = tk.StringVar(value="1000")
        silence_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.silence_threshold_var,
            width=100
        )
        silence_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Submit button
        self.submit_btn = ctk.CTkButton(
            controls_frame,
            text="Start Analysis",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.submit_analysis,
            state="disabled"
        )
        self.submit_btn.grid(row=2, column=0, pady=(0, 15))
        
    def setup_status_display_section(self):
        """Setup job status monitoring display"""
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Section title
        ctk.CTkLabel(
            status_frame, 
            text="Analysis Status", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10))
        
        # Status display
        self.status_text = ctk.CTkTextbox(
            status_frame,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.status_text.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        # Initial status
        self.update_status_display("Ready to analyze video files...")
        
    def setup_results_section(self):
        """Setup results display section"""
        results_frame = ctk.CTkFrame(self.main_frame)
        results_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=(0, 20))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Section title
        ctk.CTkLabel(
            results_frame, 
            text="Analysis Results", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10))
        
        # Results display
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 15))
        
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
            self.file_path_var.set(f"Selected: {os.path.basename(file_path)}")
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
                    timeout=5
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
            time.sleep(2)
    
    def update_job_status_display(self, status_data: Dict[str, Any]):
        """Update the status display with job information"""
        status_text = (
            f"Job ID: {status_data['job_id']}\n"
            f"Status: {status_data['status'].upper()}\n"
            f"Message: {status_data['message']}\n"
        )
        
        if status_data.get('progress'):
            status_text += f"Progress: {status_data['progress']}\n"
        
        if status_data.get('created_at'):
            status_text += f"Created: {status_data['created_at']}\n"
        
        if status_data.get('completed_at'):
            status_text += f"Completed: {status_data['completed_at']}\n"
        
        self.update_status_display(status_text)
    
    def on_job_complete(self, status_data: Dict[str, Any]):
        """Handle job completion"""
        self.stop_status_updates = True
        
        if status_data["status"] == "completed":
            self.update_status_display(
                f"✅ Analysis completed successfully!\n"
                f"Output file: {status_data.get('output_file', 'N/A')}"
            )
            
            # Display results
            if status_data.get('result'):
                self.display_results(status_data['result'])
        
        elif status_data["status"] == "failed":
            error_msg = status_data.get('error', 'Unknown error')
            self.update_status_display(f"❌ Analysis failed: {error_msg}")
        
        # Re-enable submit button
        self.submit_btn.configure(state="normal")
        self.current_job_id = None
    
    def display_results(self, result_data: Dict[str, Any]):
        """Display analysis results"""
        self.results_text.delete("1.0", tk.END)
        
        # Format results nicely
        results_text = "=== ANALYSIS RESULTS ===\n\n"
        results_text += f"File: {result_data.get('file_name', 'N/A')}\n"
        results_text += f"FPS: {result_data.get('fps', 'N/A')}\n"
        results_text += f"Duration (frames): {result_data.get('duration_frames', 'N/A')}\n"
        results_text += f"Speakers: {', '.join(result_data.get('speakers', []))}\n"
        
        # Count words and silence periods
        words = result_data.get('words', [])
        word_count = len([w for w in words if w.get('word') != '**SILENCE**'])
        silence_count = len([w for w in words if w.get('word') == '**SILENCE**'])
        
        results_text += f"Words: {word_count}\n"
        results_text += f"Silence periods: {silence_count}\n\n"
        
        # Show transcript preview (first 500 characters)
        full_transcript = result_data.get('full_transcript', '')
        if full_transcript:
            results_text += "=== TRANSCRIPT PREVIEW ===\n"
            results_text += full_transcript[:500]
            if len(full_transcript) > 500:
                results_text += "...\n\n[Transcript truncated for display]"
        
        self.results_text.insert("1.0", results_text)
    
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
