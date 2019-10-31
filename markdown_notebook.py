from libs.base import BaseApp
from main import __version__ as app_version
from uix.startscreen import StartScreen


class MarkdownNotebook(BaseApp):
    title = 'Markdown Notebook'

    def build(self):
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer
        self.screen.ids.base.init(self)
        self.screen.ids.about.init(app_version, self.theme_cls.primary_color)

        return self.screen

    def show_about(self, *args):
        self.nav_drawer.toggle_nav_drawer()

        self.manager.current = 'about'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen()]]
