from environment import BlackJackEnv
from src.agent import Agent,AgentType

# Create a Blackjack environment
env = BlackJackEnv(seats_count=7,chip_amounts=[100,100,100,100,100,100,100],render_mode="human",fps=1)
observation = env.reset()
episode_count = 0

# Set the render mode to "human" or "cmd"
env.render()

# Create an agent with the strategy
agent = Agent(strategy=AgentType.WIKIPEDIA,action_space=env.action_space)

while episode_count < 100:


    action = agent.act(int(observation[0]['dealer_card']), int(observation[0]['player_sum']))
    observation, reward, done, _, info = env.step(action)
    env.render()

    if done:
        episode_count += 1
        observation = env.reset(full_reset=False)
        env.render()


print("Episode Count: ", episode_count)
print("Played hands: ", env.played_hands)
print("Win: ", env.win)
print("Loss: ", env.loss)
print("Draw: ", env.draw)
print("Win rate: ", env.win/env.played_hands)
print("Loss rate: ", env.loss/env.played_hands)
print("Draw rate: ", env.draw/env.played_hands)

env.close()
