from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import json
import os

DATA_DIR = os.path.expanduser("~/.fpe_companion")
os.makedirs(DATA_DIR, exist_ok=True)
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

class FPEApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#17212b')
        self.avatar_path = self.load_settings().get("avatar", "")
        self.history = self.load_history()
        
        root = BoxLayout(orientation='vertical')
        
        header = BoxLayout(size_hint_y=None, height=60, spacing=10, padding=5)
        if self.avatar_path and os.path.exists(self.avatar_path):
            self.avatar_img = Image(source=self.avatar_path, size_hint_x=None, width=50)
        else:
            self.avatar_img = Image(source="", size_hint_x=None, width=50)
        header.add_widget(self.avatar_img)
        
        title = Label(text="Aiden", bold=True, color=get_color_from_hex('#ffffff'), halign='left')
        header.add_widget(title)
        
        btn_avatar = Button(text="Фото", size_hint_x=None, width=70, background_color=get_color_from_hex('#242f3d'))
        btn_avatar.bind(on_release=self.pick_avatar)
        header.add_widget(btn_avatar)
        
        btn_3d = Button(text="3D", size_hint_x=None, width=50, background_color=get_color_from_hex('#242f3d'))
        btn_3d.bind(on_release=self.show_3d_popup)
        header.add_widget(btn_3d)
        
        root.add_widget(header)
        
        self.scroll = ScrollView()
        self.chat_box = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=10)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.scroll.add_widget(self.chat_box)
        root.add_widget(self.scroll)
        
        for msg in self.history:
            self.add_msg(msg["sender"], msg["text"], save=False)
        
        input_box = BoxLayout(size_hint_y=None, height=50, spacing=5, padding=5)
        self.input = TextInput(multiline=False, background_color=get_color_from_hex('#242f3d'), foreground_color=get_color_from_hex('#ffffff'))
        btn_send = Button(text="➤", size_hint_x=None, width=50, background_color=get_color_from_hex('#64b5ef'))
        btn_send.bind(on_release=self.send_msg)
        self.input.bind(on_text_validate=self.send_msg)
        input_box.add_widget(self.input)
        input_box.add_widget(btn_send)
        root.add_widget(input_box)
        
        if not self.history:
            self.add_msg("Aiden", "Я здесь.")
        
        return root

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception: pass
        return {}

    def save_settings(self):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"avatar": self.avatar_path}, f, ensure_ascii=False)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception: pass
        return []

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False)

    def add_msg(self, sender, text, save=True):
        lbl = Label(text=f"[b]{sender}:[/b] {text}", markup=True, size_hint_y=None, text_size=(Window.width * 0.9, None), halign='left', color=get_color_from_hex('#ffffff'))
        lbl.bind(texture_size=lbl.setter('size'))
        self.chat_box.add_widget(lbl)
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)
        
        if save:
            self.history.append({"sender": sender, "text": text})
            self.save_history()

    def send_msg(self, instance):
        text = self.input.text.strip()
        if not text: return
        self.input.text = ""
        self.add_msg("Вы", text)
        Clock.schedule_once(lambda dt: self.add_msg("Aiden", "..."), 1.0)

    def pick_avatar(self, instance):
        content = BoxLayout(orientation='vertical')
        fc = FileChooserListView(path=os.path.expanduser("~"))
        content.add_widget(fc)
        
        btn_select = Button(text="Выбрать", size_hint_y=None, height=40)
        def select(btn):
            if fc.selection:
                self.avatar_path = fc.selection[0]
                self.avatar_img.source = self.avatar_path
                self.avatar_img.reload()
                self.save_settings()
                popup.dismiss()
        btn_select.bind(on_release=select)
        content.add_widget(btn_select)
        
        popup = Popup(title="Выбери фото", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def show_3d_popup(self, instance):
        popup = Popup(title="3D Модели",
                      content=Label(text="3D-движок (Unity/VRM)\nбудет добавлен в следующем обновлении.\nСейчас доступны только фото."),
                      size_hint=(0.7, 0.4))
        popup.open()

if __name__ == '__main__':
    FPEApp().run()
