import optuna
import torch as th
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy
from src.environment import BlackJackEnv
import torch as th

if th.cuda.is_available():
    print("CUDA is available! Training on GPU.")
else:
    print("CUDA is not available! Training on CPU.")
# Optuna objective fonksiyonunu tanımlıyoruz
def objective(trial):
    # Hyperparametreleri Optuna'dan öneriyoruz
    learning_rate = trial.suggest_float('learning_rate', 1e-6, 1e-2, log=True)
    n_steps = trial.suggest_int('n_steps', 2, 2048, log=True)
    batch_size = trial.suggest_int('batch_size', 2, 1024, log=True)
    gamma = trial.suggest_float('gamma', 0.9, 0.9999)
    gae_lambda = trial.suggest_float('gae_lambda', 0.8, 1.0)
    ent_coef = trial.suggest_float('ent_coef', 1e-8, 0.1, log=True)
    clip_range = trial.suggest_float('clip_range', 0.1, 0.4)
    vf_coef = trial.suggest_float('vf_coef', 0.1, 0.9)
    max_grad_norm = trial.suggest_float('max_grad_norm', 0.3, 5.0)
    net_arch = trial.suggest_categorical('net_arch', ['large'])

    # Ağ mimarisi seçenekleri
    net_arch_options = {
        'large': [192, 384, 192]
    }

    # Policy kwargs ayarları
    policy_kwargs = dict(
        activation_fn=th.nn.ReLU,
        net_arch=net_arch_options[net_arch]
    )

    # Özel ortam
    env = BlackJackEnv(envV=3, seats_count=1, chip_amounts=[100])
    env = Monitor(env)  # Performans izleme için ortamı sarmalıyoruz

    # PPO modelini Optuna'dan gelen hyperparametrelerle oluşturuyoruz
    model = PPO('MultiInputPolicy', env,
                learning_rate=learning_rate,
                n_steps=n_steps,
                gamma=gamma,
                gae_lambda=gae_lambda,
                ent_coef=ent_coef,
                clip_range=clip_range,
                vf_coef=vf_coef,
                max_grad_norm=max_grad_norm,
                batch_size=batch_size,
                policy_kwargs=policy_kwargs,
                verbose=0,
                device='cuda')

    # Modeli belirli bir adımda değerlendiriyoruz
    eval_env = BlackJackEnv(envV=3, seats_count=1, chip_amounts=[100])
    eval_callback = EvalCallback(eval_env, best_model_save_path='./logs/',
                                 log_path='./logs/', eval_freq=2000,
                                 deterministic=True, render=False)

    model.learn(total_timesteps=20000, callback=eval_callback)

    # Modelin ortalama ödülünü değerlendiriyoruz
    mean_reward, _ = evaluate_policy(model, eval_env, n_eval_episodes=1000)

    return mean_reward

# Optuna study'si oluşturma ve optimize etme
study = optuna.create_study(direction='maximize', study_name="PPO_Env3", storage="sqlite:///optuna_study.db", load_if_exists=True)
study.optimize(objective, n_trials=100)

# En iyi hyperparametreleri yazdırıyoruz
print('Best hyperparameters: ', study.best_params)
