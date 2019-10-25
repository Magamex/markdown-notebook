from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from markdown_tree_parser.parser import parse_file

from my.widget import FileManager, NoteTreeViewLabel


class BaseScreen(Screen):

    Builder.load_file("my/basescreen.kv")

    note_tree = ObjectProperty()
    note_viewer = ObjectProperty()
    note_editor = ObjectProperty()

    def init(self, app):
        self.app = app
        self.main_screen = app.screen
        self._create_file_manager()
        self.note_tree.bind(minimum_height=self.note_tree.setter('height'))
        self.note_editor.bind(minimum_height=self.note_editor.setter('height'))
        if True:
            self._open_note_tree('/home/phpusr/notes/knowledge-base/linux.md')
            self._open_note_viewer(list(self.note_tree.iterate_all_nodes())[4].note.full_source)

    def _create_file_manager(self):
        self.file_manager = FileManager(
            root_path='/home/phpusr/notes',
            select_file_callback=self._open_note_tree,
            exit_from_app=self._exit_from_app
        )
        self.ids['fm'].add_widget(self.file_manager)
        self.file_manager.show_root()

    def _open_note_tree(self, note_file_path):
        self._fill_tree_view(note_file_path)
        self.ids.manager.current = 'note_tree_screen'
        self.main_screen.ids.action_bar.left_action_items = [
            ['chevron-left', lambda x: self._back_screen()]
        ]

    def _fill_tree_view(self, note_file_path):
        out = parse_file(note_file_path)
        self._depopulate_note_tree()
        self._populate_tree_view(out)

    def _populate_tree_view(self, node, parent=None):
        if parent is None:
            tree_node = self.note_tree.add_node(NoteTreeViewLabel(node.root, is_open=True))
        else:
            tree_node = self.note_tree.add_node(NoteTreeViewLabel(node, is_open=False), parent)

        for child_node in node:
            self._populate_tree_view(child_node, tree_node)

    def _depopulate_note_tree(self):
        for node in self.note_tree.iterate_all_nodes():
            self.note_tree.remove_node(node)

    def _select_note_heading(self, node):
        self._open_note_viewer(node.note.full_source)

    def _open_note_viewer(self, text):
        self.note_viewer.text = text
        self.ids.manager.current = 'note_viewer_screen'
        self.main_screen.ids.action_bar.left_action_items = [
            ['chevron-left', lambda x: self._back_screen()]
        ]

    def _open_note_editor(self):
        self.note_editor.text = self.note_viewer.text
        self.note_editor.cursor = (0, 0)
        self.ids.manager.current = 'note_editor_screen'
        self.main_screen.ids.action_bar.left_action_items = [
            ['chevron-left', lambda x: self._back_screen()]
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

    def _exit_from_app(self):
        self.app.dialog_exit()
