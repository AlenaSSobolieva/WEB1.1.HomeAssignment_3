from pathlib import Path
import shutil
import sys
import re


class FileOrganizer:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        self.CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
        self.LATIN_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
                              "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji",
                              "g")
        self.TRANSLITERATION = {}
        self.init_transliteration()

        self.REGISTERED_EXTENSIONS = {
            'JPEG': self.JPEG_IMAGES,
            'PNG': self.PNG_IMAGES,
            'JPG': self.JPG_IMAGES,
            'SVG': self.SVG_IMAGES,
            'AVI': self.AVI_VIDEO,
            'MP4': self.MP4_VIDEO,
            'MOV': self.MOV_VIDEO,
            'MKV': self.MKV_VIDEO,
            'DOC': self.DOC_DOCUMENTS,
            'DOCX': self.DOCX_DOCUMENTS,
            'TXT': self.TXT_DOCUMENTS,
            'PDF': self.PDF_DOCUMENTS,
            'XLSX': self.XLSX_DOCUMENTS,
            'PPTX': self.PPTX_DOCUMENTS,
            'MP3': self.MP3_MUSIC,
            'OGG': self.OGG_MUSIC,
            'WAV': self.WAV_MUSIC,
            'AMR': self.AMR_MUSIC,
            'ZIP': self.ZIP_ARCHIVE,
            'GZ': self.GZ_ARCHIVE,
            'TAR': self.TAR_ARCHIVE,
        }

        self.FOLDERS = []
        self.EXTENSIONS = set()  # only unique
        self.UNDEFINED = set()  # only unique

    def init_transliteration(self):
        for cs, ls in zip(self.CYRILLIC_SYMBOLS, self.LATIN_SYMBOLS):
            self.TRANSLITERATION[ord(cs)] = ls  # for small letters
            self.TRANSLITERATION[ord(cs.upper())] = ls.upper()  # for capital letters

    def normalize(self, name: str) -> str:
        transliterated_name = name.translate(self.TRANSLITERATION)  # for small and capital letters
        transliterated_name = re.sub(r'\W', '_', transliterated_name)
        return transliterated_name

    def define_extension(self, filename: str) -> str:
        return Path(filename).suffix[1:].upper()  # without full stop and in capital letters

    def scanning(self):
        for el in self.folder_path.iterdir():
            if el.is_dir():
                if el.name not in ('archives', 'video', 'audio', 'documents', 'images', 'other files'):
                    self.FOLDERS.append(el)
                    self.scanning(el)
                continue

            ext = self.define_extension(el.name)
            fullname = self.folder_path / el.name

            if not ext:
                self.MY_OTHERS.append(fullname)
            else:
                try:
                    container = self.REGISTERED_EXTENSIONS[ext]
                    self.EXTENSIONS.add(ext)
                    container.append(fullname)
                except KeyError:
                    self.UNDEFINED.add(ext)
                    self.MY_OTHERS.append(fullname)

    def handle_media(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / self.normalize(filename.name))

    def handle_other(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / self.normalize(filename.name))

    def handle_archive(self, filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.normalize(filename.name.replace(filename.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)

        try:
            shutil.unpack_archive(filename, folder_for_file)
        except shutil.ReadError:
            print('It is not an archive')
            folder_for_file.rmdir()
        filename.unlink()

    def handle_folder(self, folder: Path):
        try:
            folder.rmdir()
        except OSError:
            print(f'Cannot delete this folder: {folder}')

    def organize_files(self):
        self.scanning()

        for file_list, subfolder in [
            (self.JPEG_IMAGES, 'images/JPEG'),
            (self.PNG_IMAGES, 'images/PNG'),
            (self.JPG_IMAGES, 'images/JPG'),
            (self.SVG_IMAGES, 'images/SVG'),
            (self.AVI_VIDEO, 'video/AVI'),
            (self.MP4_VIDEO, 'video/MP4'),
            (self.MOV_VIDEO, 'video/MOV'),
            (self.MKV_VIDEO, 'video/MKV'),
            (self.DOC_DOCUMENTS, 'documents/DOC'),
            (self.DOCX_DOCUMENTS, 'documents/DOCX'),
            (self.TXT_DOCUMENTS, 'documents/TXT'),
            (self.PDF_DOCUMENTS, 'documents/PDF'),
            (self.XLSX_DOCUMENTS, 'documents/XLSX'),
            (self.PPTX_DOCUMENTS, 'documents/PPTX'),
            (self.MP3_MUSIC, 'audio/MP3'),
            (self.OGG_MUSIC, 'audio/OGG'),
            (self.WAV_MUSIC, 'audio/WAV'),
            (self.AMR_MUSIC, 'audio/AMR'),
            (self.MY_OTHERS, 'other files'),
            (self.ZIP_ARCHIVE, 'archives/ZIP'),
            (self.GZ_ARCHIVE, 'archives/GZ'),
            (self.TAR_ARCHIVE, 'archives/TAR')
        ]:
            for file in file_list:
                self.handle_media(file, self.folder_path / subfolder)

        for folder in self.FOLDERS[::-1]:
            self.handle_folder(folder)


def start():
    try:
        if sys.argv[1]:
            folder_for_scan = Path(sys.argv[1])
            print(f'Start in folder: {folder_for_scan}')
            organizer = FileOrganizer(folder_for_scan)
            organizer.organize_files()
    except IndexError as err:
        print(f'You should enter the name of the directory to clean it.')


if __name__ == '__main__':
    start()
