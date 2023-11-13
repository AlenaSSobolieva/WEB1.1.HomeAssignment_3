from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil
import sys
import re


class Transliterator:
    def __init__(self):
        self.CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
        self.LATIN_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
                              "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji",
                              "g")
        self.TRANSLITERATION = {}
        self.init_transliteration()

    def init_transliteration(self):
        for cs, ls in zip(self.CYRILLIC_SYMBOLS, self.LATIN_SYMBOLS):
            self.TRANSLITERATION[ord(cs)] = ls
            self.TRANSLITERATION[ord(cs.upper())] = ls.upper()

    def transliterate(self, name: str) -> str:
        transliterated_name = name.translate(self.TRANSLITERATION)
        return re.sub(r'\W', '_', transliterated_name)


class FileClassifier:
    def __init__(self):
        self.REGISTERED_EXTENSIONS = {
            'JPEG': 'images/JPEG',
            'PNG': 'images/PNG',
            'JPG': 'images/JPG',
            'SVG': 'images/SVG',
            'AVI': 'video/AVI',
            'MP4': 'video/MP4',
            'MOV': 'video/MOV',
            'MKV': 'video/MKV',
            'DOC': 'documents/DOC',
            'DOCX': 'documents/DOCX',
            'TXT': 'documents/TXT',
            'PDF': 'documents/PDF',
            'XLSX': 'documents/XLSX',
            'PPTX': 'documents/PPTX',
            'MP3': 'audio/MP3',
            'OGG': 'audio/OGG',
            'WAV': 'audio/WAV',
            'AMR': 'audio/AMR',
            'ZIP': 'archives/ZIP',
            'GZ': 'archives/GZ',
            'TAR': 'archives/TAR',
        }

    def classify_file(self, extension: str) -> str:
        return self.REGISTERED_EXTENSIONS.get(extension, 'other files')


class FileHandler:
    def __init__(self, transliterator: Transliterator, classifier: FileClassifier):
        self.transliterator = transliterator
        self.classifier = classifier

    def handle_media(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)

        # Check if the source file exists before attempting to replace it
        if filename.exists():
            new_filename = target_folder / self.transliterator.transliterate(filename.name)
            filename.replace(new_filename)
        else:
            print(f"Source file {filename} does not exist.")

    def handle_other(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)

        # Print debug information
        print(f"Current working directory: {Path.cwd()}")
        print(f"Does {filename} exist? {filename.exists()}")

        # Ensure the file exists before attempting to replace it
        if filename.exists():
            new_filename = target_folder.joinpath(self.transliterator.transliterate(filename.name))
            filename.replace(new_filename)
        else:
            print(f"Source file {filename} does not exist.")

    def handle_archive(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.transliterator.transliterate(filename.stem)
        folder_for_file.mkdir(exist_ok=True, parents=True)

        try:
            shutil.unpack_archive(filename, folder_for_file)
        except shutil.ReadError:
            print('It is not an archive')
            folder_for_file.rmdir()

        # Check if the folder exists before attempting to list files
        if folder_for_file.exists():
            files_in_folder = list(folder_for_file.iterdir())
            if not files_in_folder:
                print(f"No files found in target folder {folder_for_file}.")
            else:
                print(f"Files in target folder {folder_for_file}: {files_in_folder}")

        # Check if the original file exists before attempting to unlink
        if filename.exists():
            filename.unlink()
        else:
            print(f"File {filename} does not exist.")

class FileOrganizer:
    EXTENSIONS = set()

    def __init__(self, folder_path: Path, handler: FileHandler):
        self.folder_path = folder_path
        self.handler = handler
        self.transliterator = Transliterator()
        self.classifier = FileClassifier()

    def define_extension(self, filename: str) -> str:
        return Path(filename).suffix[1:].upper()

    def process_folder(self, folder_path: Path):
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                ext = self.define_extension(file_path.name)
                container = self.classifier.classify_file(ext)
                self.EXTENSIONS.add(ext)
                getattr(self.handler, f'handle_{container}')(file_path, self.folder_path / container)

    def organize_files(self):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_folder, subfolder) for subfolder in self.folder_path.iterdir() if subfolder.is_dir()]
            list(as_completed(futures))


def start():
    try:
        if sys.argv[1]:
            folder_for_scan = Path(sys.argv[1])
            print(f'Start in folder: {folder_for_scan}')
            file_handler = FileHandler(Transliterator(), FileClassifier())
            organizer = FileOrganizer(folder_for_scan, file_handler)
            organizer.organize_files()
    except IndexError as err:
        print(f'{err} You should enter the name of the directory to clean it.')


if __name__ == '__main__':
    start()
