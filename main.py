import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.image import Image
import grafiikat

class Taloudenhallintasovellus(App):
    def __init__(self):
        super().__init__()



    def build(self):
        uusi = grafiikat.Kaaviot()
        grafiikat.Kaaviot.create_grafic_name_and_sum(uusi)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Massikamu')
        layout.add_widget(label)
        image = Image(source="graafi.png")
        image2 = Image(source="graafi2.png")
        layout.add_widget(image)
        layout.add_widget(image2)
        
        
        return layout


if __name__ == '__main__':
    Taloudenhallintasovellus().run()