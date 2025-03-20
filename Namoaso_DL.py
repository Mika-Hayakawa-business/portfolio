from gym import spaces
import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque

class NamoasoGame:
    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=5, shape=(6,), dtype=np.int8)
        # 計6つの手が、それぞれ0~5の範囲をとる
        # spaces.Box を使うと、強化学習エージェントが観測する環境の状態を定義できる
            # low=0 → 状態の最小値が0
            # high=5 → 状態の最大値が5
            # shape=(6,) → 6次元の観測空間
            # dtype=np.int8 → 各値のデータ型（整数 int8）
        self.action_space = spaces.Discrete(9)  # 9種類の行動
        # action_space → 可能な行動の数
        # spaces.Discrete(9) → 0 から 8 の 9 種類の行動が選択可能
        self.reset()
    
    def reset(self):
        """ゲームの初期化。init関数内で使用"""

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

        self.update_state()
        return self.get_state()
        
        
    def update_state(self):
        """ 状態を辞書とNumPy配列で更新 """
        self.turn_list = {"turn": self.turn}
        self.state = self.hand_1 | self.hand_2 | self.turn_list

        self.state_tuple = np.array([
            self.hand_1.get('a', 0), self.hand_1.get('b', 0), self.hand_1.get('c', 0),
            self.hand_2.get('A', 0), self.hand_2.get('B', 0), self.hand_2.get('C', 0)
        ], dtype=np.int8)
        
        
    def get_state(self):
        """ 現在の状態をNumPy配列で取得 """
        self.update_state()
        return self.state_tuple

        
    
    def step(self, action):
        """ 1ターン進める """
        actions = [
            ("a", "A"), ("a", "B"), ("a", "C"),
            ("b", "A"), ("b", "B"), ("b", "C"),
            ("c", "A"), ("c", "B"), ("c", "C")
        ]

        if action < 0 or action >= len(actions):
            return self.get_state(), -5000, True, {}  # 無効な行動のペナルティ

        attacker, defender = actions[action]

        # 無効な手のチェック（0の手は使えない）
        if attacker not in self.hand_1 or self.hand_1[attacker] == 0:
            print(f"無効な行動: {attacker} は0なので選択できません")
            return self.get_state(), -50, True, {}  # 大きなペナルティを与える

        if defender not in self.hand_2:
            return self.get_state(), -50, True, {}  # 無効な行動

        # 手の更新（指の本数を足す）
        self.hand_2[defender] += self.hand_1[attacker]
        if self.hand_2[defender] > 4:
            self.hand_2[defender] %= 5
        if self.hand_2[defender] == 0:
            del self.hand_2[defender]  # 手が消えた場合

        # 状態更新
        self.update_state()

        # 勝敗チェック
        if not self.hand_1:
            return self.get_state(), -10, True, {}  # Player1敗北
        if not self.hand_2:
            return self.get_state(), 10, True, {}   # AI敗北

        # 報酬設計（学習を進めるために変更）
        reward = 0.2  # 通常の行動には小さな報酬を与える
        if len(self.hand_2) < 3:  # 相手の手を減らしたらボーナス
            reward += 3
        if len(self.hand_1) > len(self.hand_2):  # 手の数が相手より多いならボーナス
            reward += 3
            
        return self.get_state(), reward, False, {}
        


class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNAgent:
    def __init__(self, state_size, action_size, gamma=0.95, alpha=0.001, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma  
        self.epsilon = epsilon  
        self.epsilon_min = epsilon_min  
        self.epsilon_decay = epsilon_decay  
        self.memory = deque(maxlen=2000)
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=alpha)
        self.criterion = nn.SmoothL1Loss()  # Huber損失

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def train(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state).unsqueeze(0)
                target += self.gamma * torch.max(self.model(next_state)).item()
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state)
            target_f = q_values.clone()
            target_f[0][action] = target
            loss = self.criterion(q_values, target_f)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def load_model(self, filepath):
        """学習済みモデルをロード"""
        self.model.load_state_dict(torch.load(filepath))
        self.model.eval()  # 評価モードに変更
            
            
env = NamoasoGame()
agent = DQNAgent(state_size=env.observation_space.shape[0], action_size=env.action_space.n)

num_episodes = 1000
batch_size = 32

for episode in range(num_episodes):
    state = env.reset()
    done = False
    episode_reward = 0
    
    while not done:
        action = agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        episode_reward += reward
    
    agent.train(batch_size)

    if episode % 1000 == 0:
        print(f"Episode {episode}/{num_episodes}, Reward: {episode_reward}")

torch.save(agent.model.state_dict(), "dqn_namoaso.pth")