import os

from kivymd.uix.filemanager import MDFileManager


class FileManager(MDFileManager):

    def __init__(self, code_input, root_path):
        super().__init__(
            exit_manager=self.exit_manager_call,
            select_path=self.select_path_call,
            previous=False
        )
        self.code_input = code_input
        self.root_path = root_path

    def show_root(self):
        self.show(self.root_path)

    def exit_manager_call(self, *args):
        print('> exit_manager()')

    def select_path_call(self, path):
        with open(path) as f:
            self.code_input.text = f.read()

    def select_dir_or_file(self, path):
        if os.path.isfile(path):
            self.select_path(path)
            return

        self.current_path = path
        self.show(path)

    def back(self):
        if self.current_path != self.root_path:
            super().back()


