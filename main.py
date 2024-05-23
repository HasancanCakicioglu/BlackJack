from stable_baselines3 import PPO,DQN

from src.environment import BlackJackEnv

# Kaydedilmiş modeli yükle
#model = DQN.load("saved_model_1_DQN.zip")
model = PPO.load("PPO_100_000-0.3_3")

# Create a Blackjack environment
env = BlackJackEnv(seats_count=3,chip_amounts=[100,100,100],render_mode="human",fps=0.5)
observation = env.reset()[0]
episode_count = 0

# Set the render mode to "human" or "cmd"
env.render()


while episode_count < 10_000:

    action = model.predict(observation)
    observation, reward, done, _, info = env.step(action[0])
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
print("Win rate: ", env.win/env.played_hands)
print("Loss rate: ", env.loss/env.played_hands)
print("Draw rate: ", env.draw/env.played_hands)
print("Illegal Moves: ", env.illegal_moves)


# Ortamı kapat
env.close()
