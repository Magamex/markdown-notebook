from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from my.file_manager import FileManager


class BaseScreen(Screen):

    Builder.load_file("my/basescreen.kv")

    def init(self, app):
        self.app = app
        self.main_screen = app.screen
        self.create_file_manager()

    def create_file_manager(self):
        self.file_manager = FileManager(
            root_path='/home/phpusr/notes',
            open_note_editor=self.open_note_editor,
            exit_from_app=self.exit_from_app
        )
        self.ids['fm'].add_widget(self.file_manager)
        self.file_manager.show_root()

    def open_note_editor(self, note_file):
        with open(note_file) as f:
            self.ids.note_editor.text = f.read()
            self.ids.manager.current = 'note_editor_screen'
            self.main_screen.ids.action_bar.left_action_items = [
                ['chevron-left', lambda x: self.back_screen()]
            ]

    def back_screen(self):
        self.ids.manager.current = 'fm_screen'
        self.main_screen.ids.action_bar.left_action_items = [
            ['menu', lambda x: self.main_screen.ids.nav_drawer._toggle()]
        ]

    def exit_from_app(self):
        self.app.dialog_exit()
