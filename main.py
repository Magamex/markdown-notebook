import kivy
from kivy.config import Config

kivy.require('1.9.2')
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('kivy', 'log_enable', 0)

__version__ = '0.1'

if __name__ in ('__main__', '__android__'):
    try:
        from markdown_notebook import MarkdownNotebook
        app = MarkdownNotebook()
        app.run()
    except Exception as e:
        from error_app import ErrorApp
        ErrorApp(e).run()
