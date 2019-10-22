import os

from kivymd.uix.filemanager import MDFileManager


class FileManager(MDFileManager):

    def __init__(self, root_path, open_note_editor, exit_from_app):
        super().__init__(
            exit_manager=self.exit_manager_call,
            select_path=self.select_path_call,
            previous=False
        )
        self.root_path = root_path
        self.open_note_editor = open_note_editor
        self.exit_from_app = exit_from_app

    def show_root(self):
        self.show(self.root_path)

    def exit_manager_call(self, *args):
        self.exit_from_app()

    def select_path_call(self, path):
        self.open_note_editor(path)

    def select_dir_or_file(self, path):
        if os.path.isfile(path):
            self.select_path(path)
            return

        self.current_path = path
        self.show(path)

    def back(self):
        if self.current_path != self.root_path:
            super().back()


