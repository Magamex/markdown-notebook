from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class ErrorApp(App):

    def __init__(self, error):
        super().__init__()
        self.error = error

    def build(self):
        return ErrorWindow(str(self.error))


class ErrorWindow(BoxLayout):

    def __init__(self, error_message):
        self.error_message = error_message
        super().__init__()


Builder.load_string('''
<ErrorWindow>:
    orientation: 'vertical'
    padding: dp(10)
    
    Label:
        text: '[b]Error:[/b]'
        font_size: '16sp' 
        size_hint: 1, 0.1
        markup: True
    
    ScrollView:
        id: e_scroll
        scroll_y: 0
    
        TextInput:
            text: root.error_message
            size_hint_y: None
            height: max(e_scroll.height, self.minimum_height)
            background_color: 1, 1, 1, 0.9
            foreground_color: 0, 0, 0, 1
            readonly: True
''')
