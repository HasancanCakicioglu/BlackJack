import datetime

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import torch as th

from config import CHECKPOINT_DIR, LOG_DIR
from src.callbacks.trainAndLogging import TrainAndLoggingCallback
from src.environment import BlackJackEnv
import torch as th

if th.cuda.is_available():
    print("CUDA is available! Training on GPU.")
else:
    print("CUDA is not available! Training on CPU.")



callback = TrainAndLoggingCallback(check_freq=100_000, save_path=CHECKPOINT_DIR, verbose=1)
env = BlackJackEnv(envV=3, seats_count=1, chip_amounts=[100])

# Monitor wrapper ile env sarmalama
env = Monitor(env, LOG_DIR)

policy_kwargs = dict(
    activation_fn=th.nn.ReLU,
    net_arch=[
        dict(pi=[192, 384, 192], vf=[192, 384, 192])  # Politika ve Değer ağları için büyük mimari
    ]
)

#model = PPO("MultiInputPolicy", env, verbose=1 ,tensorboard_log=LOG_DIR,ent_coef=0.1,learning_rate=0.00003,policy_kwargs=policy_kwargs,batch_size=512,device="cuda")
model = PPO.load("src/models/custom_model_new_env3_ppo_1_000_000.zip",env=env,ent_coef=0.01,learning_rate=0.0003)
print(model.policy)

model.learn(total_timesteps=4_000_000, callback=callback,tb_log_name=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
model.save("src/models/custom_model_new_env3_ppo_5_000_000.zip")