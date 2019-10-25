import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from markdown_tree_parser.parser import parse_file

from my.widget import FileManager, NoteTreeViewLabel


class BaseScreen(Screen):

    Builder.load_file("my/basescreen.kv")

    note_tree = ObjectProperty()
    note_viewer = ObjectProperty()
    note_title = ObjectProperty()
    note_editor = ObjectProperty()

    def init(self, app):
        self.app = app
        self.main_screen = app.screen
        self._create_file_manager()
        self.note_tree.bind(minimum_height=self.note_tree.setter('height'))
        self.note_editor.bind(minimum_height=self.note_editor.setter('height'))
        if True:
            self._open_note_tree('/home/phpusr/notes/knowledge-base/linux.md')
            self._select_note_heading(list(self.note_tree.iterate_all_nodes())[4])
            self._open_note_editor()

    def _create_file_manager(self):
        self.file_manager = FileManager(
            root_path='/home/phpusr/notes',
            select_file_callback=self._open_note_tree,
            exit_from_app=self._exit_from_app
        )
        self.ids['fm'].add_widget(self.file_manager)
        self.file_manager.show_root()

    def _open_note_tree(self, note_file_path):
        self._current_note_file_path = note_file_path
        self._current_note_file_name = os.path.dirname(note_file_path)
        self._fill_tree_view(note_file_path)
        self.ids.manager.current = 'note_tree_screen'
        self._set_back_button()

    def _fill_tree_view(self, note_file_path):
        out = parse_file(note_file_path)
        self._depopulate_note_tree()
        self._populate_tree_view(out)

    def _populate_tree_view(self, node, parent=None):
        if parent is None:
            tree_node = self.note_tree.add_node(NoteTreeViewLabel(node.main, is_open=True))
        else:
            tree_node = self.note_tree.add_node(NoteTreeViewLabel(node, is_open=False), parent)

        for child_node in node:
            self._populate_tree_view(child_node, tree_node)

    def _depopulate_note_tree(self):
        for node in self.note_tree.iterate_all_nodes():
            self.note_tree.remove_node(node)

    def _select_note_heading(self, node):
        self._current_note = node.note
        self._open_note_viewer(node.note.full_source)

    def _open_note_viewer(self, text):
        self.note_viewer.text = text
        self.ids.manager.current = 'note_viewer_screen'
        self._set_back_button()

    def _open_note_editor(self):
        self.note_title.text = self._current_note.text
        self.note_editor.text = self._current_note.source
        self.note_editor.cursor = (0, 0)
        self.ids.manager.current = 'note_editor_screen'
        self._set_back_button(action=self._confirm_save_note)

    def _set_back_button(self, action=None):
        if action is None:
            action = self._back_screen
        self.main_screen.ids.action_bar.left_action_items = [
            ['chevron-left', lambda x: action()]
        ]

    def _back_screen(self):
        manager = self.ids.manager
        if manager.current == 'note_editor_screen':
            manager.current = 'note_viewer_screen'
        elif manager.current == 'note_viewer_screen':
            manager.current = 'note_tree_screen'
        elif manager.current == 'note_tree_screen':
            manager.current = 'fm_screen'
            self.main_screen.ids.action_bar.left_action_items = [
                ['menu', lambda x: self.main_screen.ids.nav_drawer._toggle()]
            ]
        else:
            raise Exception('Not support screen')

    def _confirm_save_note(self):
        if self.note_title.text == self._current_note.text \
                and self.note_editor.text == self._current_note.source:
            self._back_screen()
            return

        MDDialog(
            title='Confirm save',
            size_hint=(0.8, 0.3),
            text_button_ok='Yes',
            text_button_cancel='No',
            text=f'Do you want to save {self._current_note_file_name}',
            events_callback=self._confirm_save_note_callback
        ).open()

    def _confirm_save_note_callback(self, answer, _):
        if answer == 'Yes':
            self._current_note.text = self.note_title.text
            self._current_note.source = self.note_editor.text
            with open(self._current_note_file_path, 'w') as f:
                f.write(self._current_note.root.full_source)
                self._back_screen()
        elif answer == 'No':
            self._back_screen()

    def _exit_from_app(self):
        self.app.dialog_exit()
