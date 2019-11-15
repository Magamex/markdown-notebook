import os
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.modalview import ModalView
from kivy.uix.treeview import TreeViewLabel
from kivymd.uix.dialog import MDDialog

from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import TwoLineListItem


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


class LongpressMixin:
    __events__ = ('on_long_press', 'on_short_press')

    long_press_time = Factory.NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            self._clockev = Clock.schedule_once(self._do_long_press, self.long_press_time)
        else:
            if self._clockev.is_triggered == 1:
                self.dispatch('on_short_press')
            self._clockev.cancel()

    def _do_long_press(self, long_press_time):
        self.dispatch('on_long_press', long_press_time)

    def on_long_press(self, long_press_time):
        raise NotImplementedError

    def on_short_press(self):
        raise NotImplementedError


class NotebookListItem(LongpressMixin, TwoLineListItem):
    def __init__(self, remove_item_callback, select_item_callback, **kwargs):
        super(NotebookListItem, self).__init__(**kwargs)
        self.remove_item = remove_item_callback
        self.select_item = select_item_callback

    def on_long_press(self, long_press_time):
        MDDialog(
            title='Delete notebook', size_hint=(.8, .3),
            text_button_ok='Yes', text_button_cancel='No',
            text=f'Are you sure to delete "{self.secondary_text}" notebook?',
            events_callback=self.dialog_callback
        ).open()

    def on_short_press(self):
        self.select_item(self.secondary_text)

    def dialog_callback(self, value, dialog):
        if value == 'Yes':
            self.remove_item(self, self.secondary_text)

    def events_callback(self, value):
        pass


class NotebooksSelectorModalView(ModalView):
    class FileManager(MDFileManager):
        def __init__(self, root_path, add_notebook, **kwargs):
            super().__init__(**kwargs)
            self.current_path = root_path
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

    def build(self, root_path, add_notebook):
        self.file_manager = NotebooksSelectorModalView.FileManager(
            root_path=root_path,
            exit_manager=self.exit_manager,
            add_notebook=add_notebook
        )
        self.add_widget(self.file_manager)

    def open(self):
        super().open()
        self.file_manager.show()

    def exit_manager(self, _):
        self.dismiss()

