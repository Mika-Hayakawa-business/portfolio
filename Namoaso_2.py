from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
import japanize_kivy
import random

class FingerGameScreen_2(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("namoaso_2.kv")  # kvファイルの正確な名前を指定
    
    def on_enter(self):
        self.init_game()
        self.update_font_size()  # 初期フォントサイズを設定
        Window.bind(size=self.update_font_size)  # 画面サイズ変更時にフォントサイズを更新
        
    def update_font_size(self, *args):
        # 画面サイズに応じてフォントサイズを調整する
        base_size = min(Window.width, Window.height) * 0.05  # 全体の5%を基準とする

        # 各ラベルの文字サイズを調整
        self.ids.timer_label_1.font_size = base_size * 1.5
        self.ids.timer_label_2.font_size = base_size * 1.5
        self.ids.status_label_1.font_size = base_size * 1.0
        self.ids.status_label_2.font_size = base_size * 1.0
        self.ids.next_button_1.font_size = base_size * 1.0
        self.ids.next_button_2.font_size = base_size * 1.0

    def init_game(self):
        # ゲームの初期化
        self.turn = random.randint(1, 2)
        self.o = random.randint(1, 3)
        self.p = random.randint(1, 3)
        self.q = random.randint(1, 3)
        self.r = random.randint(1, 3)
        
        # 不正な組み合わせの回避
        if self.o == 3 and self.q == 2:
            self.o = random.randint(1, 2)
        if self.o == 2 and self.q == 3:
            self.q = random.randint(1, 2)
        if self.o == 3 and self.r == 2:
            self.o = random.randint(1, 2)
        if self.o == 2 and self.r == 3:
            self.r = random.randint(1, 2)
        if self.p == 3 and self.q == 2:
            self.p = random.randint(1, 2)
        if self.p == 2 and self.q == 3:
            self.q = random.randint(1, 2)
        if self.p == 3 and self.r == 2:
            self.p = random.randint(1, 2)
        if self.p == 2 and self.r == 3:
            self.r = random.randint(1, 2)

        # 初期手の設定
        self.hand_1 = {'a': 1, 'b': self.o, 'c': self.p}
        self.hand_2 = {'A': 1, 'B': self.q, 'C': self.r}
        self.timer_seconds = 15
        self.selected_input_1 = None
        self.selected_input_2 = None
        
        # 初回のターンタイマーを開始
        self.update_hand_display()
        self.start_timer()

    def start_timer(self):
        # 現在のターンに応じて、該当するタイマーを開始
        if self.turn == 1:  # Player 1 のターン
            self.ids.status_label_1.text = "あなたのターン"
            self.ids.status_label_2.text = "相手のターン"
            Clock.unschedule(self.update_timer_2)
            Clock.schedule_interval(self.update_timer_1, 1)
            self.ids.next_button_2.disabled = True
        else:  # Player 2 のターン
            self.ids.status_label_1.text = "相手のターン"
            self.ids.status_label_2.text = "あなたのターン"
            Clock.unschedule(self.update_timer_1)
            Clock.schedule_interval(self.update_timer_2, 1)
            self.ids.next_button_1.disabled = True

    def update_timer_1(self, dt):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.ids.timer_label_1.text = f"{self.timer_seconds}"
        else:
            self.ids.status_label_1.text = "タイムアップ！\nあなたの負けです"
            self.ids.status_label_2.text = "あなたの勝ちです"
            Clock.unschedule(self.update_timer_1)
            self.ids.next_button_1.disabled = True
            self.ids.next_button_2.disabled = True
            
    def update_timer_2(self, dt):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.ids.timer_label_2.text = f"{self.timer_seconds}"
        else:           
            self.ids.status_label_1.text = "あなたの勝ちです"
            self.ids.status_label_2.text = "タイムアップ！\nあなたの負けです"
            Clock.unschedule(self.update_timer_2)
            self.ids.next_button_1.disabled = True
            self.ids.next_button_2.disabled = True

    def update_hand_display(self):
        try:
            self.ids.player1_a.background_normal = f"hand_{self.hand_1.get('a', 0)}.png"
        except KeyError:
            pass  # 何もしない
        try:
            self.ids.player1_b.background_normal = f"hand_{self.hand_1.get('b', 0)}.png"
        except KeyError:
            pass  # 何もしない

        try:
            self.ids.player1_c.background_normal = f"hand_{self.hand_1.get('c', 0)}.png"
        except KeyError:
            pass  # 何もしない

        try:
            self.ids.player2_A.background_normal = f"hand_{self.hand_2.get('A', 0)}.png"
        except KeyError:
            pass  # 何もしない

        try:
            self.ids.player2_B.background_normal = f"hand_{self.hand_2.get('B', 0)}.png"
        except KeyError:
            pass  # 何もしない

        try:
            self.ids.player2_C.background_normal = f"hand_{self.hand_2.get('C', 0)}.png"
        except KeyError:
            pass  # 何もしない
    
    def on_image_tap_1(self, image_id):
    # 以前の選択をリセットする
        if self.selected_input_1:
        # 以前の選択を通常の画像に戻す
            previous_id = self.selected_input_1
            if previous_id in self.hand_1:  # キーが存在するかを確認
                self.ids[f"player1_{previous_id}"].background_normal = f"hand_{self.hand_1[previous_id]}.png"
            else:
                pass  # 何もしない

    # 新しい選択を保存する
        self.selected_input_1 = image_id

    # 新しい選択された画像を選択状態の画像に変更する
        if image_id in self.hand_1:  # キーが存在するかを確認
            self.ids[f"player1_{image_id}"].background_normal = f"hand_{self.hand_1[image_id]}_select.png"
        else:
            pass  # 何もしない

    def on_image_tap_2(self, image_id):
    # 以前の選択をリセットする
        if self.selected_input_2:
        # 以前の選択を通常の画像に戻す
            previous_id = self.selected_input_2
            if previous_id in self.hand_2:  # キーが存在するかを確認
                self.ids[f"player2_{previous_id}"].background_normal = f"hand_{self.hand_2[previous_id]}.png"
            else:
                pass  # 何もしない

    # 新しい選択を保存する
        self.selected_input_2 = image_id

    # 新しい選択された画像を選択状態の画像に変更する
        if image_id in self.hand_2:  # キーが存在するかを確認
            self.ids[f"player2_{image_id}"].background_normal = f"hand_{self.hand_2[image_id]}_select.png"
        else:
            pass  # 何もしない
    
    def next_turn(self):
        # 必要なチェックと引き分けの判定は同じです
        if self.timer_seconds <= 0 or not self.selected_input_1 or not self.selected_input_2:
            return

        # 各プレイヤーの手を適切に更新するロジックはそのまま
        if self.turn == 1:
            player_input_1 = self.selected_input_1
            player_input_2 = self.selected_input_2
            if player_input_1 in self.hand_1 and player_input_2 in self.hand_2:
                self.hand_2[player_input_2] += self.hand_1[player_input_1]
                if self.hand_2[player_input_2] > 4:
                    self.hand_2[player_input_2] %= 5
                if self.hand_2[player_input_2] == 0:
                    del self.hand_2[player_input_2]
            else:
                self.ids.status_label_1.text = "無効な入力です"
            self.ids.next_button_2.disabled = False
            self.turn = 2
        else:
            player_input_1 = self.selected_input_1
            player_input_2 = self.selected_input_2
            if player_input_2 in self.hand_2 and player_input_1 in self.hand_1:
                self.hand_1[player_input_1] += self.hand_2[player_input_2]
                if self.hand_1[player_input_1] > 4:
                    self.hand_1[player_input_1] %= 5
                if self.hand_1[player_input_1] == 0:
                    del self.hand_1[player_input_1]
            else:
                self.ids.status_label_2.text = "無効な入力です"
            self.ids.next_button_1.disabled = False
            self.turn = 1

        # ゲームの状態を更新
        self.update_hand_display()
        self.timer_seconds = 15  # タイマーをリセット
        self.selected_input_1 = None
        self.selected_input_2 = None

        # 引き分けチェック: 両手が1本ずつ残り、特定の手の値の場合
        hand_1_values = list(self.hand_1.values())
        hand_2_values = list(self.hand_2.values())

        if (len(hand_1_values) == 1 and len(hand_2_values) == 1 and
                ((hand_1_values == [1] and hand_2_values == [2]) or
                 (hand_1_values == [3] and hand_2_values == [1]) or
                 (hand_1_values == [2] and hand_2_values == [4]) or
                 (hand_1_values == [4] and hand_2_values == [3]))):
            self.ids.status_label_1.text = "引き分けです"
            self.ids.status_label_2.text = "引き分けです"
            # タイマー停止とボタン無効化
            Clock.unschedule(self.update_timer_1)
            Clock.unschedule(self.update_timer_2)
            self.ids.next_button_1.disabled = True
            self.ids.next_button_2.disabled = True
            return  # 引き分けが確定したので次の処理を行わない

        # 勝敗判定：手がなくなった場合に勝敗を確定
        if not self.hand_1:
            self.ids.status_label_1.text = "あなたの負けです"
            self.ids.status_label_2.text = "あなたの勝ちです"
            Clock.unschedule(self.update_timer_1)
            Clock.unschedule(self.update_timer_2)
            self.ids.next_button_1.disabled = True
            self.ids.next_button_2.disabled = True
        elif not self.hand_2:
            self.ids.status_label_1.text = "あなたの勝ちです"
            self.ids.status_label_2.text = "あなたの負けです"
            Clock.unschedule(self.update_timer_1)
            Clock.unschedule(self.update_timer_2)
            self.ids.next_button_1.disabled = True
            self.ids.next_button_2.disabled = True
        else:
            self.start_timer()  # 次のターンのタイマーを開始