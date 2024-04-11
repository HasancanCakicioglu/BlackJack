from environment import BlackJackEnv
from src.agent import Agent,AgentType

# Create a Blackjack environment
env = BlackJackEnv(seats_count=2,chip_amounts=[100,100])
observation = env.reset()
episode_count = 0

# Set the render mode to "human" or "cmd"
render = "human" # "human" or "cmd"
env.render(mode=render)

# Create an agent with the strategy
agent = Agent(strategy=AgentType.RANDOM,action_space=env.action_space)

while episode_count < 100:

    action = agent.act(observation[0], observation[1])
    observation, reward, done, _, info = env.step(action)
    env.render(mode=render)

    if done:
        episode_count += 1
        observation = env.reset(full_reset=False)
        env.render(mode=render)


print("Episode Count: ", episode_count)
print("Played hands: ", env.played_hands)
print("Win: ", env.win)
print("Loss: ", env.loss)
print("Draw: ", env.draw)
print("Win rate: ", env.win/env.played_hands)
print("Loss rate: ", env.loss/env.played_hands)
print("Draw rate: ", env.draw/env.played_hands)

env.close()
