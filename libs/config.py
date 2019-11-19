from libs.error import MessageError

GENERAL_SECTION = 'General'
NOTEBOOKS_OPTION = 'notebooks'
CURRENT_NOTEBOOK_OPTION = 'current_notebook'
CURRENT_NOTE_OPTION = 'current_note'
SPLITTER = ';'

THEME_SECTION = 'Theme'
STYLE_OPTION = 'style'
PRIMARY_PALETTE_OPTION = 'primary_palette'
ACCENT_PALETTE_OPTION = 'accent_palette'


class MarkdownNotebookConfig:
    def __init__(self, config):
        self.config = config
        for section in [GENERAL_SECTION, THEME_SECTION]:
            config.adddefaultsection(section)

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

    def load_theme(self, theme_cls):
        theme_cls.theme_style = self.config.getdefault(THEME_SECTION, STYLE_OPTION, 'Light')
        theme_cls.primary_palette = self.config.getdefault(THEME_SECTION, PRIMARY_PALETTE_OPTION, 'Blue')
        theme_cls.accent_palette = self.config.getdefault(THEME_SECTION, ACCENT_PALETTE_OPTION, 'Pink')

    def set_theme(self, theme_cls):
        self.config.set(THEME_SECTION, STYLE_OPTION, theme_cls.theme_style)
        self.config.set(THEME_SECTION, PRIMARY_PALETTE_OPTION, theme_cls.primary_palette)
        self.config.set(THEME_SECTION, ACCENT_PALETTE_OPTION, theme_cls.accent_palette)
        self.config.write()
