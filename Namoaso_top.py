from kivy.config import Config
Config.set('input', 'wm_touch', 'null')
Config.set('input', 'wm_pen', 'null')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from Namoaso_2 import FingerGameScreen_2  # 分離したゲーム画面のクラスをインポート
from Namoaso_1_A import FingerGameScreen_1_A  # 分離したゲーム画面のクラスをインポート

class TopScreen(Screen):
    pass

class NamoasoTop(App):
    def build(self):
        # ウィンドウサイズ設定
        Window.size = (1280, 720)
        Builder.load_file("namoaso_top.kv")
        Builder.load_file("namoaso_2.kv")
        Builder.load_file("namoaso_1_A.kv")

        # ScreenManager を作成
        sm = ScreenManager()
        sm.add_widget(TopScreen(name="top"))
        sm.add_widget(FingerGameScreen_2(name="finger_game_2"))
        sm.add_widget(FingerGameScreen_1_A(name="finger_game_1_A"))

        return sm

if __name__ == "__main__":
    NamoasoTop().run()