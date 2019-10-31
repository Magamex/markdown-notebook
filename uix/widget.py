import os
from kivy.uix.treeview import TreeViewLabel

from kivymd.uix.filemanager import MDFileManager


class FileManager(MDFileManager):

    def __init__(self, root_path, select_file_callback, exit_manager_callback):
        super().__init__(previous=False)
        self.root_path = root_path
        self.select_file_callback = select_file_callback
        self.exit_manager_callback = exit_manager_callback

    def show_root(self):
        self.show(self.root_path)

    def select_path(self, path):
        self.select_file_callback(path)

    def select_dir_or_file(self, path):
        if os.path.isfile(path):
            self.select_path(path)
            return

        self.current_path = path
        self.show(path)

    def back(self):
        if self.current_path != self.root_path:
            super().back()

    def exit_manager(self, _):
        self.exit_manager_callback()

    def refresh(self):
        self.show(self.current_path)


class NoteTreeViewLabel(TreeViewLabel):

    def __init__(self, note, **kwargs):
        super().__init__(text=note.text, **kwargs)
        self.note = note
