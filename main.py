from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter
import sv_ttk
from PIL import Image
import os
import subprocess
import datetime
import piexif
import json

#create root window
root = tkinter.Tk()

#root window title and dimensions
root.title("Thumbnail and Optimize")
root.geometry("900x750")



# Configure grid columns root display
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)


# Centered header label
header = ttk.Label(root, text="Thumbnail and Optimize", font=("Helvetica", 36, "bold"))
header.grid(row=0, column=0, columnspan=5, pady=(40, 20), sticky="n")

# Source folder input
def browse_source():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_var.set(folder_selected)

source_var = StringVar()


# Source folder input frame (centered)
source_frame = ttk.Frame(root, padding="5", borderwidth=2, relief="groove")
source_frame.grid(row=1, column=1, pady=10, sticky="ew")
source_inp = ttk.Entry(source_frame, textvariable=source_var, width=40, font=("Helvetica", 10))
source_inp.grid(row=0, column=0, padx=10, pady=10)
source_inp.insert(0, 'Select Source Folder')
browse_btn = ttk.Button(source_frame, text="Browse", command=browse_source)
browse_btn.grid(row=0, column=1, padx=10)
source_frame.configure(style="Card.TFrame")

# Destination folder input
def browse_dest():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        dest_var.set(folder_selected)

dest_var = StringVar()


# Destination folder input frame (centered below source)
dest_frame = ttk.Frame(root, padding="5", borderwidth=2, relief="groove")
dest_frame.grid(row=1, column=3, pady=10, sticky="ew")
dest_inp = ttk.Entry(dest_frame, textvariable=dest_var, width=40, font=("Helvetica", 10))
dest_inp.grid(row=0, column=0, padx=10, pady=10)
dest_inp.insert(0, 'Select Destination Folder')
browse_btn2 = ttk.Button(dest_frame, text="Browse", command=browse_dest)
browse_btn2.grid(row=0, column=1, padx=10)
dest_frame.configure(style="Card.TFrame")


# Image Output Options (quality / output format / width / height)

options_frame = ttk.Frame(root, padding="5", borderwidth=2, relief="groove")
options_frame.grid(row=2, column=0, columnspan=5, pady=10, padx=10, sticky="ew")
options_frame.configure(style="Card.TFrame")



# Output Dropdown Menu
options = ["JPEG", "PNG", "WEBP", "JPG"]

output_format_label = ttk.Label(options_frame, text="Output Format:")
output_format_label.grid(row=0, column=0, pady=10, sticky="w")
output_format_var = StringVar(value="JPEG")
output_format_menu = ttk.OptionMenu(options_frame, output_format_var, output_format_var.get(), *options)
output_format_menu.grid(row=1, column=0, pady=10, sticky="ew")

# Quality Slider
quality_label = ttk.Label(options_frame, text="Image Quality:")
quality_label.grid(row=0, column=1, pady=10, padx=(20,0), sticky="w")
quality_var = tkinter.IntVar(value=50)
quality_str = tkinter.StringVar(value=str(quality_var.get()))
def update_quality_label(val):
    quality_str.set(str(int(float(val))))
quality_slider = ttk.Scale(options_frame, from_=30, to=80, orient="horizontal", variable=quality_var, command=update_quality_label, length=250)
quality_slider.grid(row=1, column=1, pady=10, padx=(20,0), sticky="ew")
quality_value_label = ttk.Label(options_frame, textvariable=quality_str)
quality_value_label.grid(row=1, column=2, padx=(5,0), sticky="w")

# Resize Options
resize_width_var = tkinter.StringVar(value="")
resize_height_var = tkinter.StringVar(value="")
resize_label = ttk.Label(options_frame, text="Resize (px):")
resize_label.grid(row=0, column=3, padx=(20,0), pady=10, sticky="w")
resize_width_entry = ttk.Entry(options_frame, textvariable=resize_width_var, width=6)
resize_width_entry.grid(row=1, column=3, padx=(20,0), pady=10, sticky="w")
x_label = ttk.Label(options_frame, text="x")
x_label.grid(row=1, column=4, pady=10, sticky="w")
resize_height_entry = ttk.Entry(options_frame, textvariable=resize_height_var, width=6)
resize_height_entry.grid(row=1, column=5, pady=10, sticky="w")

# Log file management
LOG_FILE = "pixfix_log.txt"

def append_log(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}\n"
    # Keep only last 250 lines in the log file
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            lines = []
        lines.append(entry)
        lines = lines[-250:]
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception:
        pass

# Open log in new window
def open_log_window():
    log_window = tkinter.Toplevel(root)
    log_window.title("Processing Log")
    log_window.geometry("800x500")
    
    # Frame for log content
    log_frame = ttk.Frame(log_window, padding="10")
    log_frame.pack(fill="both", expand=True)
    
    # Label - increased font size
    log_label = ttk.Label(log_frame, text="Processing Log:", font=("Helvetica", 14, "bold"))
    log_label.pack(anchor="w", pady=(0, 5))
    
    # Text widget with scrollbar - larger font for better readability
    text_frame = ttk.Frame(log_frame)
    text_frame.pack(fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")
    
    log_text = tkinter.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Courier", 11))
    log_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=log_text.yview)
    
    # Load log content
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_content = f.read()
        log_text.insert("1.0", log_content)
    else:
        log_text.insert("1.0", "No log entries yet.")
    
    log_text.see("end")
    log_text.config(state="disabled")
    
    # Button frame for Close and Clear Log
    btn_frame = ttk.Frame(log_frame)
    btn_frame.pack(pady=(10, 0))

    def clear_log():
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")
        log_text.config(state="normal")
        log_text.delete("1.0", tkinter.END)
        log_text.insert("1.0", "Log cleared.")
        log_text.config(state="disabled")

    clear_btn = ttk.Button(btn_frame, text="Clear Log", command=clear_log)
    clear_btn.pack(side="left", padx=(0, 10))
    close_btn = ttk.Button(btn_frame, text="Close", command=log_window.destroy)
    close_btn.pack(side="left")

# Function to execute with both folder paths

def process_folders():
    source = source_var.get()
    dest = dest_var.get()
    # Error handling for missing source or destination folder, or if default text is present
    if not source or source == 'Select Source Folder':
        error_var.set("Please select a valid source folder.")
        loading_var.set("")
        return
    if not dest or dest == 'Select Destination Folder':
        error_var.set("Please select a valid destination folder.")
        loading_var.set("")
        return
    # Only set loading_var if both folders are selected
    if source and dest:
        loading_var.set("Processing images, please wait...")
    root.update_idletasks()
    quality = quality_var.get()
    output_format = output_format_var.get()
    
    # Get resize values (blank means no resize)
    width_str = resize_width_var.get().strip()
    height_str = resize_height_var.get().strip()
    resize_width = int(width_str) if width_str.isdigit() else None
    resize_height = int(height_str) if height_str.isdigit() else None

    success = True
    error_messages = []
    
    # Initialize counters
    processed_count = 0
    skipped_count = 0
    errored_count = 0
    total_count = 0
    
    # Check for potential overwrites in destination folder, but only for images that will be processed
    overwrite_files = []
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if not (os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))):
            continue
        
        # Check if this image would be skipped (already thumbnailed in destination)
        skip = False
        base_name, _ = os.path.splitext(filename)
        ext = output_format_var.get().lower() if output_format_var.get() != 'JPG' else 'jpg'
        output_filename = f"th_{base_name}.{ext}"
        output_path = os.path.join(dest, output_filename)
        if os.path.isfile(output_path):
            try:
                if output_filename.lower().endswith(('.jpg', '.jpeg')):
                    img_check = Image.open(output_path)
                    comment = img_check.info.get('comment', b'')
                    if isinstance(comment, bytes):
                        comment_str = comment.decode(errors='ignore').strip().lower()
                    else:
                        comment_str = str(comment).strip().lower()
                    if comment_str == 'thumbnailed':
                        skip = True
                elif output_filename.lower().endswith('.png'):
                    img_check = Image.open(output_path)
                    if 'thumbnailed' in img_check.info:
                        if img_check.info['thumbnailed'].strip().lower() == 'yes':
                            skip = True
            except Exception:
                pass
        if skip:
            continue
        base_name, _ = os.path.splitext(filename)
        ext = output_format_var.get().lower() if output_format_var.get() != 'JPG' else 'jpg'
        output_filename = f"th_{base_name}.{ext}"
        output_path = os.path.join(dest, output_filename)
        if os.path.isfile(output_path):
            overwrite_files.append(output_filename)
    if overwrite_files:
        from tkinter import messagebox
        msg = (
            "The following files already exist in the destination folder and will be overwritten:\n\n" +
            "\n".join(overwrite_files) +
            "\n\nDo you want to continue?"
        )
        if not messagebox.askokcancel("Confirm Overwrite", msg):
            error_var.set("Operation cancelled by user.")
            loading_var.set("")
            return

    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)

        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            total_count += 1
            
            # Skip files with underscores in the name
            if '_' in filename:
                append_log(f"Skipped (underscore in filename): {filename}")
                skipped_count += 1
                continue
            
            # Check if already thumbnailed in DESTINATION folder
            skip = False
            base_name, _ = os.path.splitext(filename)
            ext = output_format.lower() if output_format != 'JPG' else 'jpg'
            output_filename = f"th_{base_name}.{ext}"
            output_path = os.path.join(dest, output_filename)
            
            if os.path.isfile(output_path):
                try:
                    if output_filename.lower().endswith(('.jpg', '.jpeg')):
                        img_check = Image.open(output_path)
                        comment = img_check.info.get('comment', b'')
                        if isinstance(comment, bytes):
                            comment_str = comment.decode(errors='ignore').strip().lower()
                        else:
                            comment_str = str(comment).strip().lower()
                        if comment_str == 'thumbnailed':
                            skip = True
                    elif output_filename.lower().endswith('.png'):
                        img_check = Image.open(output_path)
                        if 'thumbnailed' in img_check.info:
                            if img_check.info['thumbnailed'].strip().lower() == 'yes':
                                skip = True
                except Exception:
                    pass
            
            if skip:
                append_log(f"Skipped (already thumbnailed): {filename}")
                skipped_count += 1
                continue
            try:
                img = Image.open(file_path)
                # Resize if values are provided
                if resize_width or resize_height:
                    orig_w, orig_h = img.size
                    new_w = resize_width if resize_width else orig_w
                    new_h = resize_height if resize_height else orig_h
                    img = img.resize((new_w, new_h), Image.LANCZOS)
                # Change output file extension to match selected format and add "th_" prefix
                base_name, _ = os.path.splitext(filename)
                ext = output_format.lower() if output_format != 'JPG' else 'jpg'
                output_filename = f"th_{base_name}.{ext}"
                output_path = os.path.join(dest, output_filename)
                # Always use the selected format for saving
                img = img.convert('RGB') if output_format.upper() in ['JPEG', 'JPG', 'WEBP', 'JPG'] else img
                
                # Add metadata: thumbnailed = yes
                meta = img.info.copy() if hasattr(img, 'info') else {}
                save_kwargs = dict(optimize=True, quality=quality, format=output_format.upper())
                if output_format.upper() in ['JPEG', 'JPG']:
                    # JPEG: Only keep the JPEG Comment (COM marker)
                    img.save(output_path, optimize=True, quality=quality, format=output_format.upper(), comment=b'thumbnailed')
                elif output_format.upper() == 'PNG':
                    from PIL.PngImagePlugin import PngInfo
                    pnginfo = PngInfo()
                    pnginfo.add_text('thumbnailed', 'yes')
                    img.save(output_path, optimize=True, quality=quality, format=output_format.upper(), pnginfo=pnginfo)
                else:
                    img.save(output_path, optimize=True, quality=quality, format=output_format.upper())
                append_log(f"Processed: {filename}")
                processed_count += 1
            except Exception as e:
                error_msg = f"Error processing {filename}: {e}"
                print(error_msg)
                error_messages.append(error_msg)
                append_log(error_msg)
                success = False
                errored_count += 1
    if success:
        loading_var.set("Processing complete! All images saved successfully.")
        error_var.set("")
        append_log("Batch complete: All images saved successfully.")
        # Remove any previous link widgets
        for widget in root.grid_slaves(row=99, column=0):
            widget.destroy()
        # Show clickable link to open destination folder - using brighter cyan for better contrast
        open_link_label = ttk.Label(root, text="Open Destination Folder", foreground="#5DADE2", cursor="hand2", font=("Helvetica", 14, "bold underline"), background=root.cget('background'))
        def open_dest_folder(event=None):
            import subprocess, os, sys
            folder = dest_var.get()
            if sys.platform.startswith('win'):
                os.startfile(folder)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', folder])
            else:
                subprocess.Popen(['xdg-open', folder])
        open_link_label.bind("<Button-1>", open_dest_folder)
        open_link_label.grid(row=99, column=0, columnspan=5, pady=(10, 20))
    else:
        loading_var.set("Processing complete with errors. See below.")
        error_var.set("\n".join(error_messages))
        append_log("Batch complete with errors.")
    
    # Update statistics table
    processed_var.set(str(processed_count))
    skipped_var.set(str(skipped_count))
    errored_var.set(str(errored_count))
    total_var.set(str(total_count))
    stats_frame.grid()  # Show the stats table
    
    root.update_idletasks()
    save_settings()

# Button to execute the function (centered)
process_btn = ttk.Button(root, text="Process Folders", command=process_folders, width=107)
process_btn.grid(row=3, column=0, columnspan=5, pady=10)

loading_var = tkinter.StringVar(value="")
loading_label = ttk.Label(root, textvariable=loading_var, font=("Helvetica", 16, "bold"))
loading_label.grid(row=4, column=0, columnspan=5, pady=10)

# Error message label (initially empty) - using brighter red for better contrast
error_var = tkinter.StringVar(value="")
error_label = ttk.Label(root, textvariable=error_var, font=("Helvetica", 13), foreground="#FF6B6B")
error_label.grid(row=5, column=0, columnspan=5, pady=(0,10))

# Processing statistics table
stats_frame = ttk.Frame(root, padding="10", borderwidth=2, relief="groove")
stats_frame.grid(row=6, column=0, columnspan=5, pady=10, padx=200, sticky="ew")
stats_frame.grid_remove()  # Hide initially
stats_frame.configure(style="Card.TFrame")

# Table headers - increased font size and bold for better visibility
ttk.Label(stats_frame, text="Processed", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=20, pady=5)
ttk.Label(stats_frame, text="Skipped", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=20, pady=5)
ttk.Label(stats_frame, text="Errored", font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=20, pady=5)
ttk.Label(stats_frame, text="Total", font=("Helvetica", 12, "bold")).grid(row=0, column=3, padx=20, pady=5)

# Table values - increased font size for better readability
processed_var = tkinter.StringVar(value="0")
skipped_var = tkinter.StringVar(value="0")
errored_var = tkinter.StringVar(value="0")
total_var = tkinter.StringVar(value="0")

ttk.Label(stats_frame, textvariable=processed_var, font=("Helvetica", 14)).grid(row=1, column=0, padx=20, pady=5)
ttk.Label(stats_frame, textvariable=skipped_var, font=("Helvetica", 14)).grid(row=1, column=1, padx=20, pady=5)
ttk.Label(stats_frame, textvariable=errored_var, font=("Helvetica", 14)).grid(row=1, column=2, padx=20, pady=5)
ttk.Label(stats_frame, textvariable=total_var, font=("Helvetica", 14)).grid(row=1, column=3, padx=20, pady=5)

# View Log button - positioned in bottom left corner
view_log_btn = ttk.Button(root, text="View Log", command=open_log_window, width=20)
view_log_btn.place(x=20, y=700)  # 20px from left, 700px from top (near bottom of 750px window)

# Theme toggle functionality
current_theme = StringVar(value="light")

def toggle_theme():
    if current_theme.get() == "dark":
        sv_ttk.set_theme("light")
        current_theme.set("light")
        theme_toggle_btn.config(text="☀️ Light Mode")
    else:
        sv_ttk.set_theme("dark")
        current_theme.set("dark")
        theme_toggle_btn.config(text="🌙 Dark Mode")

# Theme toggle button - positioned in bottom right corner
theme_toggle_btn = ttk.Button(root, text="🌙 Dark Mode", command=toggle_theme, width=20)
theme_toggle_btn.place(x=700, y=700)  # 730px from left (near right edge), 700px from top

SETTINGS_FILE = "pixfix_settings.json"

def save_settings():
    settings = {
        "source": source_var.get(),
        "dest": dest_var.get()
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f)

def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        if settings.get("source"):
            source_var.set(settings["source"])
        if settings.get("dest"):
            dest_var.set(settings["dest"])
    except Exception:
        pass

# Call load_settings() after initializing source_var and dest_var
load_settings()

sv_ttk.set_theme("dark")

#Execute Tkinter
root.mainloop()

save_settings()