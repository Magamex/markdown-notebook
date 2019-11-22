import sys

import kivy
import os
import traceback
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
    except Exception:
        directory = os.path.split(os.path.abspath(sys.argv[0]))[0]
        text_error = traceback.format_exc()
        traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))

        from libs.error_app import ErrorApp
        ErrorApp(text_error).run()
