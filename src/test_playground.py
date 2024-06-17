import numpy as np
from stable_baselines3 import PPO, DQN
from src.environment import BlackJackEnv

# Modeli yükleme
model = PPO.load(
    "playground/src/models/custom_model_new_env3_ppo_1_000_000.zip")
# Modelin gözlem uzayını al
observation_space = model.policy.observation_space

# Gözlem uzayını yazdır
print("Observation space:", observation_space)
# Blackjack ortamını oluşturma
env = BlackJackEnv(seats_count=1, chip_amounts=[100], render_mode="humjan", envV=3, fps=0.5)
observation = env.reset()[0]
episode_count = 0

# Gözlemin şekli ve türünü kontrol et
print("Initial observation:", observation)
print("Initial observation type:", type(observation))

# Set the render mode to "human" or "cmd"
env.render()

while episode_count < 100_000:

    obs_values = {
        'player_sum': observation['player_sum'],
        'dealer_card': observation['dealer_card'],
        'usable_ace': observation['usable_ace'],
        'can_split': observation['can_split'],
        'can_double': observation['can_double'],
        'two': np.array([observation['two']], dtype=np.float16),
        'three': np.array([observation['three']], dtype=np.float16),
        'four': np.array([observation['four']], dtype=np.float16),
        'five': np.array([observation['five']], dtype=np.float16),
        'six': np.array([observation['six']], dtype=np.float16),
        'seven': np.array([observation['seven']], dtype=np.float16),
        'eight': np.array([observation['eight']], dtype=np.float16),
        'nine': np.array([observation['nine']], dtype=np.float16),
        'ten': np.array([observation['ten']], dtype=np.float16),
        'ace': np.array([observation['ace']], dtype=np.float16),
        'last_card': observation['last_card']
    }

    action, _ = model.predict(obs_values)

    # Gözlem, ödül, done ve info'yu alın
    observation, reward, done, _, info = env.step(action)
    env.render()

    if done:
        episode_count += 1
        observation = env.reset(full_reset=False)[0]
        env.render()

print("Episode Count: ", episode_count)
print("Played hands: ", env.played_hands)
print("Win: ", env.win)
print("Loss: ", env.loss)
print("Draw: ", env.draw)
print("Win rate: ", env.win / env.played_hands)
print("Loss rate: ", env.loss / env.played_hands)
print("Draw rate: ", env.draw / env.played_hands)
print("Money ", env.money)
print("Earn Rate ", env.earn_money_rate)
print("Lose Rate ", env.loss_money_rate)
print("Illegal Moves: ", env.illegal_moves)

# Ortamı kapat
env.close()
