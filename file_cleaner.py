from os import scandir, rename
from os.path import exists, join, splitext
from shutil import move
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fill in the directory paths
source_dir = r"C:\Users\apani\Downloads"
dest_dir_sfx = r"D:\DOWNLOADS\sfx"
dest_dir_music = r"D:\DOWNLOADS\music"
dest_dir_video = r"D:\DOWNLOADS\video"
dest_dir_image = r"D:\DOWNLOADS\image"
dest_dir_documents = r"D:\DOWNLOADS\document"
dest_dir_zip = r"D:\DOWNLOADS\zip"
dest_dir_applications = r"D:\DOWNLOADS\setup"

# Supported file extensions
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
zip_extensions = [".zip", ".rar", ".7z", ".tar", ".gz"]
application_extensions = [".exe", ".msi", ".bat", ".cmd", ".sh"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # IF FILE EXISTS, ADD NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

def on_cleaner():
    files_moved = {
        "audio": 0,
        "video": 0,
        "image": 0,
        "document": 0,
        "zip": 0,
        "application": 0
    }
    with scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            if entry.is_file():
                files_moved["audio"] += check_audio_files(entry, name)
                files_moved["video"] += check_video_files(entry, name)
                files_moved["image"] += check_image_files(entry, name)
                files_moved["document"] += check_document_files(entry, name)
                files_moved["zip"] += check_zip_files(entry, name)
                files_moved["application"] += check_application_files(entry, name)
    
    logging.info(f"Files moved summary: {files_moved}")

def check_audio_files(entry, name):  # Checks all Audio Files
    for audio_extension in audio_extensions:
        if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
            if entry.stat().st_size < 10_000_000 or "SFX" in name:  # 10 Megabytes
                dest = dest_dir_sfx
            else:
                dest = dest_dir_music
            move_file(dest, entry, name)
            logging.info(f"Moved audio file: {name}")
            return 1
    return 0

def check_video_files(entry, name):  # Checks all Video Files
    for video_extension in video_extensions:
        if name.endswith(video_extension) or name.endswith(video_extension.upper()):
            move_file(dest_dir_video, entry, name)
            logging.info(f"Moved video file: {name}")
            return 1
    return 0

def check_image_files(entry, name):  # Checks all Image Files
    for image_extension in image_extensions:
        if name.endswith(image_extension) or name.endswith(image_extension.upper()):
            move_file(dest_dir_image, entry, name)
            logging.info(f"Moved image file: {name}")
            return 1
    return 0

def check_document_files(entry, name):  # Checks all Document Files
    for documents_extension in document_extensions:
        if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
            move_file(dest_dir_documents, entry, name)
            logging.info(f"Moved document file: {name}")
            return 1
    return 0

def check_zip_files(entry, name):  # Checks all Zip Files
    for zip_extension in zip_extensions:
        if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
            move_file(dest_dir_zip, entry, name)
            logging.info(f"Moved zip file: {name}")
            return 1
    return 0

def check_application_files(entry, name):  # Checks all Application Files
    for application_extension in application_extensions:
        if name.endswith(application_extension) or name.endswith(application_extension.upper()):
            move_file(dest_dir_applications, entry, name)
            logging.info(f"Moved application file: {name}")
            return 1
    return 0

# Call the main function to start the file organization process
if __name__ == '__main__':
    on_cleaner()
