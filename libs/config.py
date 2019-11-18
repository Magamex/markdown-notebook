from libs.error import MessageError

GENERAL_SECTION = 'General'
NOTEBOOKS_OPTION = 'notebooks'
CURRENT_NOTEBOOK_OPTION = 'current_notebook'
CURRENT_NOTE_OPTION = 'current_note'
SPLITTER = ';'


class MarkdownNotebookConfig:
    def __init__(self, config):
        self.config = config

    @property
    def notebook_paths(self):
        paths_str = self.config.getdefault(GENERAL_SECTION, NOTEBOOKS_OPTION, '')
        paths = paths_str.split(SPLITTER) if paths_str != '' else []
        return paths

    def add_notebook_path(self, path):
        paths = self.notebook_paths
        if path in paths:
            raise MessageError('Notebook already added')

        paths.append(path)
        self.config.set(GENERAL_SECTION, NOTEBOOKS_OPTION, SPLITTER.join(paths))
        self.config.write()

    def remove_notebook_path(self, path):
        paths = self.notebook_paths
        if path in paths:
            paths.remove(path)
            self.config.set(GENERAL_SECTION, NOTEBOOKS_OPTION, SPLITTER.join(paths))
            self.config.write()

    @property
    def current_notebook(self):
        return self.config.getdefault(GENERAL_SECTION, CURRENT_NOTEBOOK_OPTION, None)

    def set_current_notebook(self, notebook_path):
        self.config.set(GENERAL_SECTION, CURRENT_NOTEBOOK_OPTION, notebook_path)
        self.config.write()

    @property
    def current_note(self):
        return self.config.getdefault(GENERAL_SECTION, CURRENT_NOTE_OPTION, None)

    def set_current_note(self, note_path):
        self.config.set(GENERAL_SECTION, CURRENT_NOTE_OPTION, note_path)
        self.config.write()
