from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class ErrorApp(App):

    def __init__(self, error):
        super().__init__()
        self.error = error

    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(
            markup=True,
            text='[b]Error:[/b]',
            size_hint=(1, 0.1))
        )
        layout.add_widget(Label(text=str(self.error)))
        return layout
