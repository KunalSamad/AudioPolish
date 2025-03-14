import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from processing import AudioProcessor
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk  # For progress bar

class NoiseReducerGUI(tk.Tk):
    def __init__(self, processor):
        super().__init__()
        self.title("Noise_Reducer")
        self.geometry("900x750")  # Increased size to accommodate all elements
        self.resizable(False, False)
        self.processor = processor

        # Mode variables
        self.batch_var = tk.BooleanVar(value=False)  # Batch processing mode flag

        # File/Folder paths
        self.input_path = ""      # For single file mode
        self.output_path = ""     # For single file mode
        self.input_folder = ""    # For batch mode
        self.output_folder = ""   # For batch mode

        # --- Mode Selection ---
        mode_frame = tk.Frame(self)
        mode_frame.pack(pady=5)
        batch_cb = tk.Checkbutton(mode_frame, text="Batch Processing", variable=self.batch_var, command=self.toggle_mode)
        batch_cb.pack()

        # --- Import/Export Buttons (for single file mode) ---
        self.single_frame = tk.Frame(self)
        self.single_frame.pack(pady=10)
        self.single_frame.pack_propagate(False)
        self.single_frame.configure(width=850, height=50)
        import_btn = tk.Button(self.single_frame, text="Import Audio File", command=self.import_audio_file)
        import_btn.grid(row=0, column=0, padx=10)
        export_btn = tk.Button(self.single_frame, text="Set Output File", command=self.export_audio_file)
        export_btn.grid(row=0, column=1, padx=10)

        # --- Folder Selection Buttons (for batch mode) ---
        self.batch_frame = tk.Frame(self)
        self.batch_frame.pack_forget()
        self.batch_frame.pack_propagate(False)
        self.batch_frame.configure(width=850, height=50)
        batch_in_btn = tk.Button(self.batch_frame, text="Select Input Folder", command=self.select_input_folder)
        batch_in_btn.grid(row=0, column=0, padx=10)
        batch_out_btn = tk.Button(self.batch_frame, text="Select Output Folder", command=self.select_output_folder)
        batch_out_btn.grid(row=0, column=1, padx=10)
        open_out_folder_btn = tk.Button(self.batch_frame, text="Open Output Folder", command=self.open_output_folder)
        open_out_folder_btn.grid(row=0, column=2, padx=10)
        
        # --- Path Label ---
        self.path_label = tk.Label(self, text="No file/folder selected", wraplength=600)
        self.path_label.pack(pady=5)
        
        # --- Visualization Frames (only for single file mode) ---
        self.vis_frame_original = tk.LabelFrame(self, text="Original Audio Visualization", width=400, height=250)
        self.vis_frame_original.pack(side="left", padx=10, pady=10)
        self.vis_frame_original.pack_propagate(False)
        self.canvas_original = None

        self.vis_frame_processed = tk.LabelFrame(self, text="Processed Audio Visualization", width=400, height=250)
        self.vis_frame_processed.pack(side="right", padx=10, pady=10)
        self.vis_frame_processed.pack_propagate(False)
        self.canvas_processed = None

        # --- Operation Selection Panel ---
        op_frame = tk.LabelFrame(self, text="Select Operations", height=150)
        op_frame.pack(pady=10, fill="x", padx=10)
        op_frame.pack_propagate(False)
        self.noise_var = tk.BooleanVar(value=False)
        noise_cb = tk.Checkbutton(op_frame, text="Noise Reduction", variable=self.noise_var)
        noise_cb.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.reverb_var = tk.BooleanVar(value=False)
        reverb_cb = tk.Checkbutton(op_frame, text="Reverb Reduction", variable=self.reverb_var)
        reverb_cb.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.echo_var = tk.BooleanVar(value=False)
        echo_cb = tk.Checkbutton(op_frame, text="Echo Reduction", variable=self.echo_var)
        echo_cb.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        self.volume_norm_var = tk.BooleanVar(value=False)
        vol_norm_cb = tk.Checkbutton(op_frame, text="Volume Normalization", variable=self.volume_norm_var)
        vol_norm_cb.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        self.volume_comp_var = tk.BooleanVar(value=False)
        vol_comp_cb = tk.Checkbutton(op_frame, text="Volume Compression", variable=self.volume_comp_var)
        vol_comp_cb.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        
        # --- Process Pipeline Button ---
        process_btn = tk.Button(self, text="Apply Selected Operations", command=self.process_pipeline, width=25, height=2)
        process_btn.pack(pady=10)
        
        # --- Log Section ---
        log_frame = tk.LabelFrame(self, text="Operation Log", width=850, height=150)
        log_frame.pack(pady=10, padx=10)
        log_frame.pack_propagate(False)
        self.log_text = tk.Text(log_frame, wrap="word", state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll = tk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        # --- Progress Bar ---
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=5, fill="x", padx=10)
        
    def toggle_mode(self):
        if self.batch_var.get():
            self.single_frame.pack_forget()
            self.vis_frame_original.pack_forget()
            self.vis_frame_processed.pack_forget()
            self.batch_frame.pack(pady=10)
            self.path_label.config(text="Batch mode: Select input and output folders")
        else:
            self.batch_frame.pack_forget()
            self.single_frame.pack(pady=10)
            self.vis_frame_original.pack(side="left", padx=10, pady=10)
            self.vis_frame_processed.pack(side="right", padx=10, pady=10)
            self.path_label.config(text="Single file mode: Select an audio file and output file")
    
    def import_audio_file(self):
        path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.*")])
        if path:
            self.input_path = path
            self.path_label.config(text=f"Loaded file: {self.input_path}")
            try:
                self.processor.load_audio(self.input_path)
                self.plot_original_waveform()
                self.add_log(f"{os.path.basename(self.input_path)}: Imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load audio:\n{e}")
                self.add_log(f"{os.path.basename(path)}: Import failed")
        else:
            self.path_label.config(text="No file loaded")
    
    def export_audio_file(self):
        path = filedialog.asksaveasfilename(title="Save Audio File", defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if path:
            self.output_path = path
            self.path_label.config(text=f"Output set to: {self.output_path}")
            self.add_log(f"Output file set: {self.output_path}")
        else:
            self.path_label.config(text="No output file selected")
    
    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder = folder
            self.path_label.config(text=f"Input folder set: {self.input_folder}")
            self.add_log(f"Input folder selected: {self.input_folder}")
        else:
            self.path_label.config(text="No input folder selected")
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.path_label.config(text=f"Output folder set: {self.output_folder}")
            self.add_log(f"Output folder selected: {self.output_folder}")
        else:
            self.path_label.config(text="No output folder selected")
    
    def open_output_folder(self):
        if self.output_folder:
            if sys.platform == "win32":
                os.startfile(self.output_folder)
            elif sys.platform == "darwin":
                subprocess.call(["open", self.output_folder])
            else:
                subprocess.call(["xdg-open", self.output_folder])
            self.add_log("Opened output folder")
        else:
            messagebox.showwarning("Warning", "Output folder is not set.")
    
    def plot_original_waveform(self):
        if self.canvas_original:
            self.canvas_original.get_tk_widget().destroy()
        fig = Figure(figsize=(4, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.processor.audio_data, color='blue')
        ax.set_title("Original Audio")
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        ax.set_ylim([-1, 1])
        self.canvas_original = FigureCanvasTkAgg(fig, master=self.vis_frame_original)
        self.canvas_original.draw()
        self.canvas_original.get_tk_widget().pack(fill="both", expand=True)
    
    def plot_processed_waveform(self):
        if self.canvas_processed:
            self.canvas_processed.get_tk_widget().destroy()
        fig = Figure(figsize=(4, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.processor.audio_data, color='green')
        ax.set_title("Processed Audio")
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        ax.set_ylim([-1, 1])
        self.canvas_processed = FigureCanvasTkAgg(fig, master=self.vis_frame_processed)
        self.canvas_processed.draw()
        self.canvas_processed.get_tk_widget().pack(fill="both", expand=True)
    
    def add_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state="disabled")
        self.log_text.see(tk.END)
    
    def process_pipeline(self):
        # Batch mode processing.
        if self.batch_var.get():
            if not self.input_folder or not self.output_folder:
                messagebox.showwarning("Warning", "Please set both input and output folders for batch processing.")
                return
            audio_extensions = (".wav", ".mp3", ".flac", ".ogg")
            files = [f for f in os.listdir(self.input_folder) if f.lower().endswith(audio_extensions)]
            total_files = len(files)
            if total_files == 0:
                messagebox.showwarning("Warning", "No valid audio files found in the input folder.")
                return
            for idx, filename in enumerate(files):
                in_file = os.path.join(self.input_folder, filename)
                out_file = os.path.join(self.output_folder, filename)
                self.add_log(f"{filename}: Processing started")
                try:
                    proc = AudioProcessor()
                    proc.load_audio(in_file)
                    ops = []
                    if self.noise_var.get():
                        ops.append("Noise Reduction")
                    if self.echo_var.get():
                        ops.append("Echo Reduction")
                    if self.reverb_var.get():
                        ops.append("Reverb Reduction")
                    if self.volume_norm_var.get():
                        ops.append("Volume Normalization")
                    if self.volume_comp_var.get():
                        ops.append("Volume Compression")
                    order_map = {
                        "Noise Reduction": 1,
                        "Echo Reduction": 2,
                        "Reverb Reduction": 3,
                        "Volume Normalization": 4,
                        "Volume Compression": 5,
                    }
                    ops_sorted = sorted(ops, key=lambda op: order_map.get(op, 100))
                    for op in ops_sorted:
                        proc.process_operation(op)
                        self.add_log(f"{filename}: {op} Successful")
                    proc.save_audio(out_file)
                    self.add_log(f"{filename}: Saved to output folder")
                except Exception as e:
                    self.add_log(f"{filename}: Processing failed: {e}")
                # Update progress for batch mode
                progress = ((idx + 1) / total_files) * 100
                self.progress_var.set(progress)
                self.update_idletasks()
            messagebox.showinfo("Batch Processing", "Batch processing completed. Check log for details.")
            self.progress_var.set(0)
        else:
            # Single file mode.
            filename = os.path.basename(self.input_path)
            ops = []
            if self.noise_var.get():
                ops.append("Noise Reduction")
            if self.echo_var.get():
                ops.append("Echo Reduction")
            if self.reverb_var.get():
                ops.append("Reverb Reduction")
            if self.volume_norm_var.get():
                ops.append("Volume Normalization")
            if self.volume_comp_var.get():
                ops.append("Volume Compression")
            if not ops:
                messagebox.showwarning("Warning", "No operations selected")
                return
            total_ops = len(ops)
            for i, op in enumerate(ops):
                self.processor.process_operation(op)
                self.add_log(f"{filename}: {op} applied successfully")
                progress = ((i + 1) / total_ops) * 100
                self.progress_var.set(progress)
                self.update_idletasks()
            if self.output_path:
                self.processor.save_audio(self.output_path)
                self.add_log(f"{filename}: Saved to output file")
                messagebox.showinfo("Success", "Operations applied and audio saved successfully")
            else:
                messagebox.showinfo("Success", "Operations applied successfully (no output file set)")
            self.plot_processed_waveform()
            self.progress_var.set(0)

if __name__ == "__main__":
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    processor = AudioProcessor()
    app = NoiseReducerGUI(processor)
    app.mainloop()
