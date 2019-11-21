from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivymd.uix.navigationdrawer import NavigationLayout


class NavDrawer(NavigationLayout):
    Builder.load_file("uix/kv/nav_drawer.kv")

    _app = ObjectProperty()

    def _toggle(self):
        self.toggle_nav_drawer()

    def add_name_previous_screen(self):
        name_current_screen = self._app.manager.current
        if self.state == 'open':
            try:
                if self._app.previous_screens[-1] == name_current_screen:
                    return
            except IndexError:
                pass
            self._app.previous_screens.append(name_current_screen)
