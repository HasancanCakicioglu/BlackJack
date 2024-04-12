import os
import numpy as np
from gymnasium.vector.utils import spaces
from stable_baselines3.common.atari_wrappers import MaxAndSkipEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.env_checker import check_env, _check_unsupported_spaces
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import load_results
from stable_baselines3.common.results_plotter import ts2xy
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import VecMonitor, SubprocVecEnv
from src.environment import BlackJackEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor

class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq:
    :param log_dir: Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """

    def __init__(self, check_freq: int, log_dir: str, verbose: int = 1):
        super().__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, "best_model")
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:

            # Retrieve training reward
            x, y = ts2xy(load_results(self.log_dir), "timesteps")
            if len(x) > 0:
                # Mean training reward over the last 100 episodes
                mean_reward = np.mean(y[-100:])
                if self.verbose >= 1:
                    print(f"Num timesteps: {self.num_timesteps}")
                    print(
                        f"Best mean reward: {self.best_mean_reward:.2f} - Last mean reward per episode: {mean_reward:.2f}")

                # New best model, you could save the agent here
                if mean_reward > self.best_mean_reward:
                    self.best_mean_reward = mean_reward
                    # Example for saving best model
                    if self.verbose >= 1:
                        print(f"Saving new best model to {self.save_path}")
                    self.model.save(self.save_path)

        return True

def make_env(seed=0):
    env = BlackJackEnv(seats_count=1, chip_amounts=[100], render_mode="human", fps=1)
    env = Monitor(env, log_dir)
    return env

if __name__ == "__main__":
    log_dir = "tmp/"
    os.makedirs(log_dir, exist_ok=True)

    n_envs = 1

    env = make_vec_env(make_env, n_envs)


    #model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log="./board/", learning_rate=0.00001,ent_coef=0.1)
    #model = DQN("MultiInputPolicy", env, verbose=1, tensorboard_log="./board/", learning_rate=0.00001)
    model = DQN.load("saved_model_1_DQN.zip",env)

    callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir)
    model.learn(total_timesteps=200_000, callback=callback, tb_log_name="DQN_1_000_000__200_000")
    model.save("DQN_1_000_000__200_000")
    print("Model saved")
