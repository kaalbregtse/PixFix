# PixFix: Image Resize and Optimize

PixFix is a Windows desktop application for batch resizing, optimizing, and thumbnailing images. It features a user-friendly GUI built with Tkinter and supports JPEG, PNG, WEBP, and JPG formats. No Python installation is required for end users—just run the provided .exe file.

## Features
- Select source and destination folders
- Resize images to custom dimensions
- Set image quality (30-80)
- Choose output format (JPEG, PNG, WEBP, JPG)
- Skip already processed images (using metadata)
- Persistent log (last 100 lines)
- Confirmation before overwriting files
- Error handling and progress messages
- Custom icon for the executable
- Settings persistence (remembers last used folders)

## Installation
### For Developers
1. Clone the repository:
   ```
   git clone https://github.com/kaalbregtse/Image-Resize-and-Optimize.git
   cd Image-Resize-and-Optimize
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python main.py
   ```

### For End Users
- Download the latest release from the `dist` folder (e.g., `main.exe`).
- Double-click the .exe to run PixFix. No Python required.

## Packaging for Distribution
To build the .exe file:
```
pyinstaller --onefile --windowed --icon=icon.ico main.py
```
The output will be in the `dist` folder.

## Usage
1. Select a source folder containing images.
2. Select a destination folder for processed images.
3. Adjust resize options, quality, and output format as needed.
4. Click "Process Folders" to start.
5. Review logs and error messages in the app.

## Metadata
- Processed images are marked with a `thumbnailed` comment (JPEG) or text field (PNG).
- Images already marked as `thumbnailed` are skipped on future runs.

## Troubleshooting
- If the app does not start, ensure you have the required DLLs (included by PyInstaller).
- Antivirus software may flag new .exe files; this is normal for custom apps.
- For icon issues, ensure your `.ico` file is valid and in the project root.

## License
MIT

## Author
[kaalbregtse](https://github.com/kaalbregtse)
