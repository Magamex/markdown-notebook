import sys

import os
from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivymd.toast import toast

from main import __version__ as app_version
from uix.startscreen import StartScreen


class MarkdownNotebook(App):
    title = 'Markdown Notebook'
    icon = 'icon.png'
    nav_drawer = ObjectProperty()
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'

    def __init__(self, **kvargs):
        super().__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'

        self.list_previous_screens = ['base']
        self.window = Window
        self.config = ConfigParser()
        self.manager = None
        self.exit_interval = False

    def get_application_config(self):
        return super().get_application_config('{}/%(appname)s.ini'.format(self.directory))

    def build_config(self, config):
        """Создаёт файл настроек приложения markdown_notebook.ini"""

        config.adddefaultsection('General')

    def set_value_from_config(self):
        """Устанавливает значения переменных из файла настроек markdown_notebook.ini"""

        self.config.read(os.path.join(self.directory, 'markdown_notebook.ini'))

    def build(self):
        self.set_value_from_config()
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer
        self.screen.ids.base.init(self)
        self.screen.ids.about.init(app_version, self.theme_cls.primary_color)

        return self.screen

    def events_program(self, instance, keyboard, keycode, text, modifiers):
        """Вызывается при нажатии кнопки Меню или Back Key
        на мобильном устройстве."""

        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()
            self.back_screen(event=keyboard)
        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        """Менеджер экранов. Вызывается при нажатии Back Key
        и шеврона "Назад" в ToolBar."""

        # Нажата BackKey.
        if event in (1001, 27):
            if self.manager.current == 'base':
                self.dialog_exit()
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except:
                self.manager.current = 'base'
            self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = \
                [['menu', lambda x: self.nav_drawer._toggle()]]

    def show_notebook(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'base'

    def show_about(self, *args):
        self.nav_drawer.toggle_nav_drawer()

        self.manager.current = 'about'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def dialog_exit(self):
        def check_interval_press(interval):
            self.exit_interval += interval
            if self.exit_interval > 5:
                self.exit_interval = False
                Clock.unschedule(check_interval_press)

        if self.exit_interval:
            sys.exit(0)
            
        Clock.schedule_interval(check_interval_press, 1)
        toast('Press Back to Exit')
