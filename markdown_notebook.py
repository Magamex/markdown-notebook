import os
from kivy.properties import ObjectProperty
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from markdown_tree_parser.parser import parse_file
from pathlib import Path

from libs.base import BaseApp
from libs.error import MessageError
from uix.widget import NoteTreeViewLabel, NotebookSelectorModalView, NotebookListItem, \
    NoteSelectorModalView


class MarkdownNotebook(BaseApp):
    title = 'Markdown Notebook'

    notebook_selector = NotebookSelectorModalView()
    note_selector = NoteSelectorModalView()
    note_tree = ObjectProperty()
    note_viewer = ObjectProperty()
    note_title = ObjectProperty()
    note_editor = ObjectProperty()

    @property
    def name(self):
        return 'markdown_notebook'

    def __init__(self):
        super().__init__('notebooks_screen', 'Notebooks')

    def build(self):
        super().build()
        self.note_tree = self.screen.ids.note_tree
        self.note_viewer = self.screen.ids.note_viewer
        self.note_title = self.screen.ids.note_title
        self.note_editor = self.screen.ids.note_editor

        self.notebook_selector.build(root_path=str(Path.home()), add_notebook_callback=self._add_new_notebook)
        self.note_selector.build(select_note_callback=self._open_note_tree,
                                 on_close_callback=lambda: self.config.set_current_notebook(''))
        self.note_tree.bind(minimum_height=self.note_tree.setter('height'))
        self.note_editor.bind(minimum_height=self.note_editor.setter('height'))

        self._fill_notebooks_from_config()

        return self.screen

    def on_start(self):
        current_note = self.config.current_note
        current_notebook = self.config.current_notebook
        if current_note is not None and os.path.exists(current_note):
            self._open_note_tree(current_note)
            self.note_selector.fm.current_path = os.path.dirname(current_note)
        elif current_notebook is not None and os.path.exists(current_notebook):
            self._open_notebook_selector(current_notebook)
        else:
            self._open_notebooks_screen()

    def _fill_notebooks_from_config(self):
        paths = self.config.notebook_paths
        for path in paths:
            self._add_notebook_to_list(path)

    def _add_notebook_to_list(self, path):
        notebook_name = os.path.basename(path)
        self.screen.ids.notebook_list.add_widget(NotebookListItem(
            text=notebook_name,
            secondary_text=path,
            remove_item_callback=self._remove_notebook,
            select_item_callback=self._select_notebook
        ))

    def _remove_notebook(self, widget, path):
        self.config.remove_notebook_path(path)
        self.screen.ids.notebook_list.remove_widget(widget)

    def _select_notebook(self, path):
        if not os.path.exists(path):
            toast('Path doesn\'t exists')
            return

        self.config.set_current_notebook(path)
        self.note_selector.open(path)

    def _add_new_notebook(self, path):
        try:
            self.config.add_notebook_path(path)
            self._add_notebook_to_list(path)
        except MessageError as e:
            toast(e.message)

    def _open_note_tree(self, note_file_path):
        self.config.set_current_note(note_file_path)
        self.screen.ids.action_bar.title = os.path.basename(note_file_path)
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
                tree_node = self.note_tree.add_node(NoteTreeViewLabel(node.main, is_open=True,
                                                                      color=self.theme_cls.text_color))
        else:
            tree_node = self.note_tree.add_node(NoteTreeViewLabel(node, is_open=False, color=self.theme_cls.text_color),
                                                parent)

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

        if self.note_selector.is_open:
            self.note_selector.fm.back()
        elif self.notebook_selector.is_open:
            self.notebook_selector.fm.back()
        elif manager.current == 'note_editor_screen':
            self._open_note_viewer()
        elif manager.current == 'note_viewer_screen':
            self._open_note_tree(self._current_note_file_path)
        elif manager.current == 'note_tree_screen':
            self._open_notebook_selector()
        else:
            super().back_screen()

    def _open_notebook_selector(self, path=None):
        self.note_selector.open(path)
        self._open_notebooks_screen()

    def _open_notebooks_screen(self):
        self.screen.ids.action_bar.title = self.base_screen_title
        self.config.set_current_note('')
        self.manager.current = self.base_screen_name
        self.screen.ids.action_bar.left_action_items = [
            ['menu', lambda x: self.screen.ids.nav_drawer._toggle()]
        ]

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
