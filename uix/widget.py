import os
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.modalview import ModalView
from kivy.uix.treeview import TreeViewLabel
from kivymd.uix.dialog import MDDialog

from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.picker import MDThemePicker


class BaseModalView(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_open = False

    def on_open(self):
        self.is_open = True

    def on_dismiss(self):
        self.is_open = False


class NoteSelectorModalView(BaseModalView):
    class FileManager(MDFileManager):
        def __init__(self, select_file_callback, **kwargs):
            super().__init__(**kwargs)
            self.select_file_callback = select_file_callback

        def show_root(self, path=None):
            if path is not None:
                self.history = []
                self.show(path)
            else:
                if self.current_path in self.history:
                    self.history.remove(self.current_path)
                self.show(self.current_path)

        def select_dir_or_file(self, path):
            if os.path.isfile(path):
                self.select_file_callback(path)
                self.exit_manager(1)
                return

            self.current_path = path
            self.show(path)

        def select_path(self, path):
            self.exit_manager(1)

        def back(self):
            if len(self.history) == 1:
                self.exit_manager(1)
            else:
                super().back()

    def __init__(self):
        super().__init__(size_hint=(1, 1), auto_dismiss=False)

    def build(self, select_note_callback):
        self.fm = NoteSelectorModalView.FileManager(
            exit_manager=self._exit_manager_callback,
            select_file_callback=select_note_callback
        )
        self.add_widget(self.fm)

    def _exit_manager_callback(self, _):
        self.dismiss()

    def open(self, path=None):
        super().open()
        self.fm.show_root(path)


class NoteTreeViewLabel(TreeViewLabel):

    def __init__(self, note, **kwargs):
        super().__init__(text=note.text, font_size='15dp', padding=(15, 15), **kwargs)
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


class NotebookSelectorModalView(BaseModalView):
    class FileManager(MDFileManager):
        def __init__(self, root_path, select_path_callback, **kwargs):
            super().__init__(**kwargs)
            self.current_path = root_path
            self.select_path_callback = select_path_callback

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
            self.select_path_callback(path)
            self.exit_manager(1)

    def __init__(self):
        super().__init__(size_hint=(1, 1), auto_dismiss=False)

    def build(self, root_path, add_notebook_callback):
        self.fm = NotebookSelectorModalView.FileManager(
            root_path=root_path,
            exit_manager=self._exit_manager_callback,
            select_path_callback=add_notebook_callback
        )
        self.add_widget(self.fm)

    def open(self):
        super().open()
        self.fm.show()

    def _exit_manager_callback(self, _):
        self.dismiss()


class ThemePicker(MDThemePicker):
    def __init__(self, config, theme_cls):
        super().__init__()
        self.config = config
        self.theme_cls = theme_cls

    def dismiss(self):
        self.config.set_theme(self.theme_cls)
        super().dismiss()

