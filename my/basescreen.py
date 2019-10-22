from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from my.file_manager import FileManager


class BaseScreen(Screen):

    Builder.load_file("my/basescreen.kv")

    def on_enter(self, *args):
        print(self.ids)

    def on_pre_enter(self, *args):
        print(self.ids)

    def open_file_manager(self):
        self.file_manager = FileManager(self.ids.code_input, '/home/phpusr/notes')
        self.ids['fm'].add_widget(self.file_manager)
        self.file_manager.show_root()
