import os
from kivy.uix.modalview import ModalView
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


class NotebooksSelectorModalView(ModalView):
    class FileManager(MDFileManager):
        def __init__(self, add_notebook, **kwargs):
            super().__init__(**kwargs)
            self.current_path = '/home/phpusr'
            self.add_notebook = add_notebook

        def show(self, path=None):
            if path is None:
                path = self.current_path
            super().show(path)

        def select_dir_or_file(self, path):
            if os.path.isfile(path):
                return

            self.current_path = path
            self.show(path)

        def select_path(self, path):
            self.add_notebook(path)
            self.exit_manager(1)

    def __init__(self):
        super().__init__(size_hint=(1, 1), auto_dismiss=False)

    def build(self, add_notebook):
        self.file_manager = NotebooksSelectorModalView.FileManager(
            exit_manager=self.exit_manager,
            add_notebook=add_notebook
        )
        self.add_widget(self.file_manager)

    def open(self):
        super().open()
        self.file_manager.show()

    def exit_manager(self, _):
        self.dismiss()

