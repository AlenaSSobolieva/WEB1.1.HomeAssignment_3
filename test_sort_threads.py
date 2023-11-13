import unittest
from pathlib import Path
from sort_threads import FileOrganizer, FileHandler, Transliterator, FileClassifier


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.folder_path = Path("test_folder")
        self.handler = FileHandler(Transliterator(), FileClassifier())
        self.organizer = FileOrganizer(self.folder_path, self.handler)

    def tearDown(self):
        # Clean up any files or folders created during the tests
        pass

    def test_handle_archive(self):
        filename = Path("test_folder/test_file.avi")
        target_folder = self.folder_path / "video/AVI"
        self.handler.handle_archive(filename, target_folder)
        self.assertFalse(filename.exists(), f"File {filename} still exists.")
        self.assertTrue(target_folder.exists(), f"Target folder {target_folder} doesn't exist.")
        self.assertFalse(
            any(file.is_file() for file in target_folder.iterdir()),
            f"No files found in target folder {target_folder}."
        )

    def test_handle_media(self):
        filename = Path("test_folder/test_file.jpg")
        target_folder = self.folder_path / "images/JPG"
        self.handler.handle_media(filename, target_folder)
        self.assertFalse(filename.exists(), f"File {filename} still exists.")
        self.assertTrue(target_folder.exists(), f"Target folder {target_folder} doesn't exist.")
        self.assertFalse(
            any(file.is_file() for file in target_folder.iterdir()),
            f"No files found in target folder {target_folder}."
        )

    def test_handle_other(self):
        filename = Path("test_folder/test_file.txt")
        target_folder = self.folder_path / "documents/TXT"
        self.handler.handle_other(filename, target_folder)
        self.assertFalse(filename.exists(), f"File {filename} still exists.")
        self.assertTrue(target_folder.exists(), f"Target folder {target_folder} doesn't exist.")
        self.assertFalse(
            any(file.is_file() for file in target_folder.iterdir()),
            f"No files found in target folder {target_folder}."
        )

    def test_organize_files(self):
        self.organizer.organize_files()
        # Add assertions based on the expected results of organizing files


if __name__ == '__main__':
    unittest.main()
