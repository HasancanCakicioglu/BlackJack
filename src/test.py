from stable_baselines3 import PPO,DQN

from src.environment import BlackJackEnv


model = PPO.load("models/PPO_5_000_000_env1.zip")

# Create a Blackjack environment
env = BlackJackEnv(seats_count=1,chip_amounts=[100],render_mode="humanfdd",envV=1,fps=0.5)
observation = env.reset()[0]
episode_count = 0

# Set the render mode to "human" or "cmd"
env.render()


while episode_count < 100_000:

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
print("Money ",env.money)
print("Earn Rate ",env.earn_money_rate)
print("Lose Rate ",env.loss_money_rate)
print("Illegal Moves: ", env.illegal_moves)


# Ortamı kapat
env.close()
