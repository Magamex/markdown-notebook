from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.treeview import TreeViewLabel
from markdown_tree_parser.parser import parse_file

from my.widget import FileManager


class BaseScreen(Screen):

    Builder.load_file("my/basescreen.kv")

    note_tree = ObjectProperty()

    def init(self, app):
        self.app = app
        self.main_screen = app.screen
        self.create_file_manager()
        self.note_tree.bind(minimum_height=self.note_tree.setter('height'))
        if True:
            self.open_note_tree('/home/phpusr/notes/knowledge-base/linux.md')

    def create_file_manager(self):
        self.file_manager = FileManager(
            root_path='/home/phpusr/notes',
            select_file_callback=self.open_note_tree,
            exit_from_app=self.exit_from_app
        )
        self.ids['fm'].add_widget(self.file_manager)
        self.file_manager.show_root()

    def open_note_tree(self, note_file_path):
        self._fill_tree_view(note_file_path)
        self.ids.manager.current = 'note_tree_screen'
        self.main_screen.ids.action_bar.left_action_items = [
            ['chevron-left', lambda x: self.back_screen()]
        ]

    def _fill_tree_view(self, note_file_path):
        out = parse_file(note_file_path)
        self._populate_tree_view(self.note_tree, out)

    def _populate_tree_view(self, tree_view, node, parent=None):
        if parent is None:
            tree_node = tree_view.add_node(TreeViewLabel(text=node.title, is_open=True))
        else:
            tree_node = tree_view.add_node(TreeViewLabel(text=node.text, is_open=False), parent)

        for child_node in node:
            self._populate_tree_view(tree_view, child_node, tree_node)

    def open_note_editor(self, note_file_path):
        with open(note_file_path) as f:
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
