import gym
from gym import spaces
import numpy as np
import random
import time
import pickle

class NamoasoGame:
    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=5, shape=(6,), dtype=np.int8)
        self.action_space = spaces.Discrete(9)  # 9種類の行動
        self.reset()  # ゲームの初期化

    
    def reset(self):
        """ゲームの初期化"""

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
            
        self.turn = random.randint(0, 1) 
                
        self.hand_1 = {"a": 1, "b": self.o, "c": self.q}
        self.hand_2 = {"A": 1, "B": self.p, "C": self.r}

        # 初期状態を作成
        self.update_state()
        return self.get_state()
        

    def update_state(self):
        """ 状態を辞書とNumPy配列で更新 """
        self.state = {
            "hand_1": list(self.hand_1.values()),  # 例: [1, 2, 3]
            "hand_2": list(self.hand_2.values()),  # 例: [1, 2, 3]
            "turn": self.turn
        }

        self.state_tuple = np.array([
            self.hand_1.get('a', 0), self.hand_1.get('b', 0), self.hand_1.get('c', 0),
            self.hand_2.get('A', 0), self.hand_2.get('B', 0), self.hand_2.get('C', 0)
        ], dtype=np.int8)
        
        
    def get_state(self):
        """ 現在の状態をNumPy配列で取得 """
        return self.state_tuple

        
    
    def step(self, action):
        """ 1ターン進める """
        actions = [
            ("a", "A"), ("a", "B"), ("a", "C"),
            ("b", "A"), ("b", "B"), ("b", "C"),
            ("c", "A"), ("c", "B"), ("c", "C")
        ]

        if action < 0 or action >= len(actions):
            return self.get_state(), -0.5, True, {}  # 無効な行動のペナルティ

        attacker, defender = actions[action]

        # 無効な手のチェック
        if attacker not in self.hand_1 or defender not in self.hand_2:
            return self.get_state(), -0.5, True, {}  # 無効な行動

        # 手の更新（指の本数を足す）
        self.hand_2[defender] += self.hand_1[attacker]
        if self.hand_2[defender] > 4:
            self.hand_2[defender] %= 5
        if self.hand_2[defender] == 0:
            del self.hand_2[defender]  # 手が消えた場合

        # 状態更新
        self.update_state()  # ← 追加

        # 勝敗チェック
        if not self.hand_1:
            return self.get_state(), -1, True, {}  # Player1敗北
        if not self.hand_2:
            return self.get_state(), 1, True, {}   # AI敗北

        # 次のターンへ
        self.turn = 3 - self.turn
        return self.get_state(), 0, False, {}  # 継続
        
class QLearning:
    def __init__(self, action_size, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.action_size = action_size
        self.alpha = alpha      # 学習率
        self.gamma = gamma      # 割引率
        self.epsilon = epsilon  # 探索率
        self.q_table = {}       # Qテーブル

    def get_q(self, state, action):
        """ Q値を取得（未学習なら0） """
        return self.q_table.get((tuple(state), action), 0.0)

    def choose_action(self, state):
        """ ε-greedy で行動を選択 """
        if np.random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_size - 1)  # ランダム選択
        else:
            q_values = [self.get_q(state, a) for a in range(self.action_size)]
            max_q = max(q_values)
            return q_values.index(max_q)  # 最大Q値の行動を選択

    def update_q(self, state, action, reward, next_state):
        """ Qテーブルの更新 """
        max_next_q = max([self.get_q(next_state, a) for a in range(self.action_size)], default=0.0)
        self.q_table[(tuple(state), action)] = (1 - self.alpha) * self.get_q(state, action) + self.alpha * (reward + self.gamma * max_next_q)

    def save_q_table(self, filename="q_table.pkl"):
        """ Qテーブルを保存 """
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename="q_table.pkl"):
        """ Qテーブルをロード """
        try:
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            self.q_table = {}  
            
env = NamoasoGame()
agent = QLearning(action_size=env.action_space.n)

num_episodes = 10000  # 学習回数
for episode in range(num_episodes):
    state = env.reset()
    done = False

    while not done:
        action = agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.update_q(state, action, reward, next_state)
        state = next_state

    if episode % 1000 == 0:
        print(f"Episode {episode} / {num_episodes}")

agent.save_q_table()