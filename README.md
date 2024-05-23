# Custom Blackjack Environment with Reinforcement Learning

This project involves creating a custom Blackjack environment and training an AI using reinforcement learning techniques, specifically Proximal Policy Optimization (PPO) and Deep Q-Network (DQN). The goal is to teach the AI to play Blackjack and achieve the best possible win rate.

## Overview

Blackjack is a popular card game where players aim to have a hand value as close to 21 as possible without exceeding it. The game involves strategic decision-making, making it an interesting challenge for reinforcement learning algorithms.

## Environment

The custom Blackjack environment is built using Python and integrates with reinforcement learning libraries to facilitate training. The environment includes:

- A simulated deck of cards.
- Dealer and player hands.
- Actions such as "hit", "stand", "double down", and "split".
- Reward system based on the outcome of each hand.

## Reinforcement Learning Algorithms

### Proximal Policy Optimization (PPO)
PPO is a policy gradient method for reinforcement learning which uses a surrogate objective function to enable multiple epochs of updates. It is robust and efficient for a variety of tasks.

### Deep Q-Network (DQN)
DQN is a value-based method that combines Q-Learning with deep neural networks. It approximates the Q-value function to make decisions based on the expected future rewards.

## Training

The AI was trained using both PPO and DQN algorithms. The training involved running multiple episodes where the AI interacted with the environment, learning optimal strategies through trial and error.

## Results

After extensive training, the best model achieved the following performance metrics:
- **Win Rate:** 43%
- **Loss Rate:** 48%
- **Draw Rate:** 9%

These results indicate that the AI can play Blackjack competitively, though there is room for improvement.

## Usage

To run the training process and evaluate the model, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HasancanCakicioglu/Custom-BlackJack-Environment-ReinforcementLearning.git
