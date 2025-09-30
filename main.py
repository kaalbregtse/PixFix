from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter
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
root.geometry("850x750")
root.configure(bg="#2b2b2b")

# Configure grid columns root display
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# Custom dark theme colors
COLORS = {
    'bg': '#2b2b2b',
    'panel': '#363636',
    'input': '#3a3a3a',
    'input_focus': '#424242',
    'text': '#E5E5E5',
    'text_dim': '#B0B0B0',
    'button': '#6B46C1',
    'button_hover': '#7C3AED',
    'button_active': '#5B35A1',
    'error': '#FF6B6B',
    'link': '#5DADE2'
}

# Configure ttk styles for dark theme
style = ttk.Style()
style.theme_use('clam')

# Configure Frame
style.configure("TFrame", background=COLORS['bg'])
style.configure("Card.TFrame", background=COLORS['panel'], borderwidth=0)

# Configure Labels
style.configure("TLabel", background=COLORS['bg'], foreground=COLORS['text'], font=("Helvetica", 10))
style.configure("Header.TLabel", background=COLORS['bg'], foreground=COLORS['text'], font=("Helvetica", 36, "bold"))
style.configure("CardLabel.TLabel", background=COLORS['panel'], foreground=COLORS['text'])

# Configure Entry
style.configure("TEntry", fieldbackground=COLORS['input'], foreground=COLORS['text'], 
                borderwidth=0, insertcolor=COLORS['text'])
style.map("TEntry", fieldbackground=[('focus', COLORS['input_focus'])])

# Configure OptionMenu
style.configure("TMenubutton", background=COLORS['input'], foreground=COLORS['text'], 
                borderwidth=0, relief="flat", padding=5)
style.map("TMenubutton", background=[('active', COLORS['input_focus'])])

# Configure Scale
style.configure("TScale", background=COLORS['bg'], troughcolor=COLORS['panel'], 
                borderwidth=0, sliderthickness=18)

# Centered header label
header = Label(root, text="Thumbnail and Optimize", font=("Helvetica", 36, "bold"),
               bg=COLORS['bg'], fg=COLORS['text'])
header.grid(row=0, column=0, columnspan=5, pady=(40, 20), sticky="n")

# Source folder input
def browse_source():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_var.set(folder_selected)

source_var = StringVar()

# Source folder input frame (centered)
source_frame = Frame(root, bg=COLORS['panel'], padx=10, pady=10)
source_frame.grid(row=1, column=1, pady=10, sticky="ew", padx=5)

source_inp = Entry(source_frame, textvariable=source_var, width=40, font=("Helvetica", 10),
                   bg=COLORS['input'], fg=COLORS['text'], insertbackground=COLORS['text'],
                   relief="flat", highlightthickness=2, highlightbackground=COLORS['input'],
                   highlightcolor=COLORS['input_focus'])
source_inp.grid(row=0, column=0, padx=(0, 10), pady=5, ipady=5)
source_inp.insert(0, 'Select Source Folder')

def create_button(parent, text, command):
    btn = Button(parent, text=text, command=command, bg=COLORS['button'], fg=COLORS['text'],
                 font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                 padx=15, pady=8, borderwidth=0, activebackground=COLORS['button_hover'],
                 activeforeground=COLORS['text'])
    return btn

browse_btn = create_button(source_frame, "Browse", browse_source)
browse_btn.grid(row=0, column=1, pady=5)

# Destination folder input
def browse_dest():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        dest_var.set(folder_selected)

dest_var = StringVar()

# Destination folder input frame (centered below source)
dest_frame = Frame(root, bg=COLORS['panel'], padx=10, pady=10)
dest_frame.grid(row=1, column=3, pady=10, sticky="ew", padx=5)

dest_inp = Entry(dest_frame, textvariable=dest_var, width=40, font=("Helvetica", 10),
                 bg=COLORS['input'], fg=COLORS['text'], insertbackground=COLORS['text'],
                 relief="flat", highlightthickness=2, highlightbackground=COLORS['input'],
                 highlightcolor=COLORS['input_focus'])
dest_inp.grid(row=0, column=0, padx=(0, 10), pady=5, ipady=5)
dest_inp.insert(0, 'Select Destination Folder')

browse_btn2 = create_button(dest_frame, "Browse", browse_dest)
browse_btn2.grid(row=0, column=1, pady=5)

# Image Output Options (quality / output format / width / height)
options_frame = Frame(root, bg=COLORS['panel'], padx=15, pady=15)
options_frame.grid(row=2, column=0, columnspan=5, pady=10, padx=10, sticky="ew")

# Output Dropdown Menu
options = ["JPEG", "PNG", "WEBP", "JPG"]

output_format_label = Label(options_frame, text="Output Format:", bg=COLORS['panel'], 
                            fg=COLORS['text'], font=("Helvetica", 10))
output_format_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

output_format_var = StringVar(value="JPEG")
output_format_menu = ttk.OptionMenu(options_frame, output_format_var, output_format_var.get(), *options)
output_format_menu.grid(row=1, column=0, pady=5, sticky="ew")

# Quality Slider
quality_label = Label(options_frame, text="Image Quality:", bg=COLORS['panel'],
                      fg=COLORS['text'], font=("Helvetica", 10))
quality_label.grid(row=0, column=1, pady=(0, 5), padx=(20, 0), sticky="w")

quality_var = tkinter.IntVar(value=50)
quality_str = tkinter.StringVar(value=str(quality_var.get()))

def update_quality_label(val):
    quality_str.set(str(int(float(val))))

quality_slider = ttk.Scale(options_frame, from_=30, to=80, orient="horizontal", 
                          variable=quality_var, command=update_quality_label, length=250)
quality_slider.grid(row=1, column=1, pady=5, padx=(20, 0), sticky="ew")

quality_value_label = Label(options_frame, textvariable=quality_str, bg=COLORS['panel'],
                           fg=COLORS['text'], font=("Helvetica", 10))
quality_value_label.grid(row=1, column=2, padx=(5, 0), sticky="w")

# Resize Options
resize_width_var = tkinter.StringVar(value="")
resize_height_var = tkinter.StringVar(value="")

resize_label = Label(options_frame, text="Resize (px):", bg=COLORS['panel'],
                    fg=COLORS['text'], font=("Helvetica", 10))
resize_label.grid(row=0, column=3, padx=(20, 0), pady=(0, 5), sticky="w")

resize_width_entry = Entry(options_frame, textvariable=resize_width_var, width=6,
                          bg=COLORS['input'], fg=COLORS['text'], insertbackground=COLORS['text'],
                          relief="flat", highlightthickness=2, highlightbackground=COLORS['input'],
                          highlightcolor=COLORS['input_focus'])
resize_width_entry.grid(row=1, column=3, padx=(20, 0), pady=5, ipady=3)

x_label = Label(options_frame, text="x", bg=COLORS['panel'], fg=COLORS['text'])
x_label.grid(row=1, column=4, pady=5, sticky="w", padx=5)

resize_height_entry = Entry(options_frame, textvariable=resize_height_var, width=6,
                           bg=COLORS['input'], fg=COLORS['text'], insertbackground=COLORS['text'],
                           relief="flat", highlightthickness=2, highlightbackground=COLORS['input'],
                           highlightcolor=COLORS['input_focus'])
resize_height_entry.grid(row=1, column=5, pady=5, ipady=3)

# Log file management
LOG_FILE = "pixfix_log.txt"

def append_log(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}\n"
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
    log_window.geometry("800x550")
    log_window.configure(bg=COLORS['bg'])
    
    log_frame = Frame(log_window, bg=COLORS['bg'], padx=15, pady=15)
    log_frame.pack(fill="both", expand=True)
    
    log_label = Label(log_frame, text="Processing Log:", font=("Helvetica", 14, "bold"),
                     bg=COLORS['bg'], fg=COLORS['text'])
    log_label.pack(anchor="w", pady=(0, 5))
    
    text_frame = Frame(log_frame, bg=COLORS['bg'])
    text_frame.pack(fill="both", expand=True)
    
    scrollbar = Scrollbar(text_frame, bg=COLORS['panel'])
    scrollbar.pack(side="right", fill="y")
    
    log_text = Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Courier", 11),
                   bg=COLORS['input'], fg=COLORS['text'], insertbackground=COLORS['text'],
                   relief="flat", padx=10, pady=10)
    log_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=log_text.yview)
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_content = f.read()
        log_text.insert("1.0", log_content)
    else:
        log_text.insert("1.0", "No log entries yet.")
    
    log_text.see("end")
    log_text.config(state="disabled")
    
    # Button frame for Clear Log and Close buttons
    btn_frame = Frame(log_frame, bg=COLORS['bg'])
    btn_frame.pack(pady=(10, 0))
    
    def clear_log():
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")
        log_text.config(state="normal")
        log_text.delete("1.0", tkinter.END)
        log_text.insert("1.0", "Log cleared.")
        log_text.config(state="disabled")
    
    clear_btn = create_button(btn_frame, "Clear Log", clear_log)
    clear_btn.pack(side="left", padx=(0, 10))
    
    close_btn = create_button(btn_frame, "Close", log_window.destroy)
    close_btn.pack(side="left")

def process_folders():
    source = source_var.get()
    dest = dest_var.get()
    if not source or source == 'Select Source Folder':
        error_var.set("Please select a valid source folder.")
        loading_var.set("")
        return
    if not dest or dest == 'Select Destination Folder':
        error_var.set("Please select a valid destination folder.")
        loading_var.set("")
        return
    if source and dest:
        loading_var.set("Processing images, please wait...")
    root.update_idletasks()
    quality = quality_var.get()
    output_format = output_format_var.get()
    
    width_str = resize_width_var.get().strip()
    height_str = resize_height_var.get().strip()
    resize_width = int(width_str) if width_str.isdigit() else None
    resize_height = int(height_str) if height_str.isdigit() else None

    success = True
    error_messages = []
    
    processed_count = 0
    skipped_count = 0
    errored_count = 0
    total_count = 0
    
    overwrite_files = []
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if not (os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))):
            continue
        
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
            
            if '_' in filename:
                append_log(f"Skipped (underscore in filename): {filename}")
                skipped_count += 1
                continue
            
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
                if resize_width or resize_height:
                    orig_w, orig_h = img.size
                    new_w = resize_width if resize_width else orig_w
                    new_h = resize_height if resize_height else orig_h
                    img = img.resize((new_w, new_h), Image.LANCZOS)
                base_name, _ = os.path.splitext(filename)
                ext = output_format.lower() if output_format != 'JPG' else 'jpg'
                output_filename = f"th_{base_name}.{ext}"
                output_path = os.path.join(dest, output_filename)
                img = img.convert('RGB') if output_format.upper() in ['JPEG', 'JPG', 'WEBP', 'JPG'] else img
                
                meta = img.info.copy() if hasattr(img, 'info') else {}
                save_kwargs = dict(optimize=True, quality=quality, format=output_format.upper())
                if output_format.upper() in ['JPEG', 'JPG']:
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
        for widget in root.grid_slaves(row=99, column=0):
            widget.destroy()
        open_link_label = Label(root, text="Open Destination Folder", foreground=COLORS['link'], 
                               cursor="hand2", font=("Helvetica", 14, "bold", "underline"), 
                               background=COLORS['bg'])
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
    
    processed_var.set(str(processed_count))
    skipped_var.set(str(skipped_count))
    errored_var.set(str(errored_count))
    total_var.set(str(total_count))
    stats_frame.grid()
    
    root.update_idletasks()
    save_settings()

# Button to execute the function (centered)
process_btn = create_button(root, "Process Folders", process_folders)
process_btn.grid(row=3, column=0, columnspan=6, pady=10, sticky="ew", padx=120, ipady=5)

loading_var = tkinter.StringVar(value="")
loading_label = Label(root, textvariable=loading_var, font=("Helvetica", 16, "bold"),
                     bg=COLORS['bg'], fg=COLORS['text'])
loading_label.grid(row=4, column=0, columnspan=5, pady=10)

error_var = tkinter.StringVar(value="")
error_label = Label(root, textvariable=error_var, font=("Helvetica", 13), 
                   foreground=COLORS['error'], bg=COLORS['bg'])
error_label.grid(row=5, column=0, columnspan=5, pady=(0, 10))

# Processing statistics table
stats_frame = Frame(root, bg=COLORS['panel'], padx=15, pady=15)
stats_frame.grid(row=6, column=0, columnspan=5, pady=10, padx=200, sticky="ew")
stats_frame.grid_remove()

Label(stats_frame, text="Processed", font=("Helvetica", 12, "bold"), 
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=0, column=0, padx=20, pady=5)
Label(stats_frame, text="Skipped", font=("Helvetica", 12, "bold"),
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=0, column=1, padx=20, pady=5)
Label(stats_frame, text="Errored", font=("Helvetica", 12, "bold"),
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=0, column=2, padx=20, pady=5)
Label(stats_frame, text="Total", font=("Helvetica", 12, "bold"),
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=0, column=3, padx=20, pady=5)

processed_var = tkinter.StringVar(value="0")
skipped_var = tkinter.StringVar(value="0")
errored_var = tkinter.StringVar(value="0")
total_var = tkinter.StringVar(value="0")

Label(stats_frame, textvariable=processed_var, font=("Helvetica", 14),
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=1, column=0, padx=20, pady=5)
Label(stats_frame, textvariable=skipped_var, font=("Helvetica", 14),
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=1, column=1, padx=20, pady=5)
Label(stats_frame, textvariable=errored_var, font=("Helvetica", 14),
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=1, column=2, padx=20, pady=5)
Label(stats_frame, textvariable=total_var, font=("Helvetica", 14),
      bg=COLORS['panel'], fg=COLORS['text']).grid(row=1, column=3, padx=20, pady=5)

# View Log button - positioned in bottom left corner
view_log_btn = create_button(root, "View Log", open_log_window)
view_log_btn.place(x=20, y=700)

# Theme toggle functionality
current_theme = StringVar(value="dark")

def toggle_theme():
    # Light mode will be implemented later
    pass

# Theme toggle button - positioned in bottom right corner
# theme_toggle_btn = create_button(root, "☀️ Light Mode", toggle_theme)
# theme_toggle_btn.place(x=730, y=700)

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

load_settings()

root.mainloop()

save_settings()