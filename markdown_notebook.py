import sys

import os
from kivy.properties import ObjectProperty
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from markdown_tree_parser.parser import parse_file

from libs.base import BaseApp
from libs.config import MarkdownNotebookConfig
from libs.error import MessageError
from uix.widget import FileManager, NoteTreeViewLabel, NotebooksSelectorModalView, NotebookListItem


class MarkdownNotebook(BaseApp):
    title = 'Markdown Notebook'

    notebooks_selector = NotebooksSelectorModalView()
    note_tree = ObjectProperty()
    note_viewer = ObjectProperty()
    note_title = ObjectProperty()
    note_editor = ObjectProperty()

    @property
    def name(self):
        return 'markdown_notebook'

    def __init__(self):
        super().__init__('fm_screen')

    def build(self):
        super().build()
        self.custom_config = MarkdownNotebookConfig(self.config)
        self.note_tree = self.screen.ids.note_tree
        self.note_viewer = self.screen.ids.note_viewer
        self.note_title = self.screen.ids.note_title
        self.note_editor = self.screen.ids.note_editor

        self.notebooks_selector.build(add_notebook=self._add_new_notebook)
        self._build_file_manager()
        self.note_tree.bind(minimum_height=self.note_tree.setter('height'))
        self.note_editor.bind(minimum_height=self.note_editor.setter('height'))

        self._fill_notebooks_from_config()

        # TODO temp
        if not True:
            self._select_note_heading(list(self.note_tree.iterate_all_nodes())[4])
            self._open_note_editor()

        return self.screen

    def _fill_notebooks_from_config(self):
        paths = self.custom_config.notebook_paths
        for path in paths:
            self._add_notebook_to_list(path)

    def _add_notebook_to_list(self, path):
        notebook_name = os.path.basename(path)
        self.screen.ids.notebook_list.add_widget(NotebookListItem(
            text=notebook_name,
            secondary_text=path,
            remove_item_callback=self._remove_notebook
        ))

    def _remove_notebook(self, widget, path):
        self.custom_config.remove_notebook_path(path)
        self.screen.ids.notebook_list.remove_widget(widget)

    def _build_file_manager(self):
        self.file_manager = FileManager(
            root_path='/home/phpusr/notes',
            select_file_callback=self._open_note_tree,
            exit_manager_callback=lambda: sys.exit(0)
        )
        self.screen.ids['fm'].add_widget(self.file_manager)
        self.file_manager.show_root()

    def _add_new_notebook(self, path):
        try:
            self.custom_config.add_notebook_path(path)
            self._add_notebook_to_list(path)
        except MessageError as e:
            toast(e.message)

    def _open_note_tree(self, note_file_path):
        self._current_note_file_path = note_file_path
        self._current_note_file_name = os.path.basename(note_file_path)
        self._fill_tree_view(note_file_path)
        self.manager.current = 'note_tree_screen'
        self._set_back_button()

    def _fill_tree_view(self, note_file_path):
        out = parse_file(note_file_path)
        self._depopulate_note_tree()
        self._populate_tree_view(out)

    def _populate_tree_view(self, node, parent=None):
        if parent is None:
            if node.main is not None:
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
        self._open_note_viewer()

    def _open_note_viewer(self):
        self.note_viewer.text = self._current_note.full_source
        self.manager.current = 'note_viewer_screen'
        self._set_back_button()

    def _open_note_editor(self):
        self.note_title.text = self._current_note.text
        self.note_editor.text = self._current_note.source
        self.note_editor.cursor = (0, 0)
        self.manager.current = 'note_editor_screen'
        self._set_back_button(action=self._confirm_save_note)

    def _set_back_button(self, action=None):
        if action is None:
            action = self.back_screen
        self.screen.ids.action_bar.left_action_items = [
            ['chevron-left', lambda x: action()]
        ]

    def back_screen(self):
        manager = self.manager
        if manager.current == 'note_editor_screen':
            self._open_note_viewer()
        elif manager.current == 'note_viewer_screen':
            self._open_note_tree(self._current_note_file_path)
        elif manager.current == 'note_tree_screen':
            manager.current = 'fm_screen'
            self.file_manager.refresh()
            self.screen.ids.action_bar.left_action_items = [
                ['menu', lambda x: self.screen.ids.nav_drawer._toggle()]
            ]
        else:
            super().back_screen()

    def _confirm_save_note(self):
        if self.note_title.text == self._current_note.text \
                and self.note_editor.text == self._current_note.source:
            self.back_screen()
            return

        MDDialog(
            title='Confirm save',
            size_hint=(0.8, 0.3),
            text_button_ok='Yes',
            text_button_cancel='No',
            text=f'Do you want to save "{self._current_note_file_name}"',
            events_callback=self._confirm_save_note_callback
        ).open()

    def _confirm_save_note_callback(self, answer, dialog):
        if answer == 'Yes':
            self._current_note.text = self.note_title.text
            self._current_note.source = self.note_editor.text
            with open(self._current_note_file_path, 'w') as f:
                f.write(self._current_note.root.full_source)
                self.back_screen()
        elif answer == 'No':
            self.back_screen()
