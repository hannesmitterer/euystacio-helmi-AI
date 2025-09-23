from multi_agent_rl_curriculum import make_env
from stable_baselines3 import PPO

env = make_env()
model = PPO("MlpPolicy", env, learning_rate=0.0001, batch_size=64, n_epochs=2, gamma=0.99, verbose=1)
model.learn(total_timesteps=500)
print("Training complete.")