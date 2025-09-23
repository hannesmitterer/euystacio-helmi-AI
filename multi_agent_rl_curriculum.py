import gym
import numpy as np
from stable_baselines3 import PPO, MADDPG
from stable_baselines3.common.envs import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback

# Define a dynamic Multi-Agent environment with refined curriculum
class DynamicMultiAgentEnv(gym.Env):
    def __init__(self):
        super(DynamicMultiAgentEnv, self).__init__()
        self.initial_action_space = gym.spaces.Discrete(2)  # Easy task with 2 actions
        self.action_space = self.initial_action_space
        self.initial_observation_space = gym.spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32)
        self.observation_space = self.initial_observation_space

    def reset(self):
        self.state = np.array([0.5, 0.5])  # Starting state
        return self.state

    def step(self, action):
        reward = -1 if action[0] != action[1] else 1  # Reward for matching actions
        done = False
        self.state = np.array([0.5, 0.5])  # Static environment
        return self.state, reward, done, {}

    def render(self):
        print(f"Current state: {self.state}")

# Dynamic Curriculum Adjustment Based on Agent’s Performance
def adjust_curriculum(agent_performance, difficulty_level):
    """
    Adjust the environment complexity based on agent's performance.
    """
    if agent_performance > 0.8:
        if difficulty_level == 1:
            # Increase task complexity: more actions, larger state space
            env.action_space = gym.spaces.Discrete(4)
            env.observation_space = gym.spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
        elif difficulty_level == 2:
            env.action_space = gym.spaces.Discrete(5)  # Even harder actions
            env.observation_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)
    elif agent_performance > 0.5:
        # Medium difficulty: moderate task complexity
        env.action_space = gym.spaces.Discrete(3)
        env.observation_space = gym.spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)
    else:
        # Easy task: initial condition for learning
        env.action_space = gym.spaces.Discrete(2)
        env.observation_space = gym.spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32)
    return env

# Wrapping Environment for Multi-Agent Setup
def make_env():
    return DynamicMultiAgentEnv()

# Initialize environment
env = DummyVecEnv([make_env, make_env])

# Select a Model (MADDPG or PPO)
# Initialize PPO model with adjusted hyperparameters
model_ppo = PPO("MlpPolicy", env, learning_rate=0.0001, batch_size=256, n_epochs=5, gamma=0.99, clip_range=0.2, verbose=1)

# Initialize MADDPG model (uncomment to switch models)
# model_maddpg = MADDPG("MlpPolicy", env, verbose=1, learning_rate=0.0005, buffer_size=int(2e6), batch_size=256, gamma=0.99)

# Set up evaluation callback to monitor agent performance during training
eval_callback = EvalCallback(env, best_model_save_path='./logs/', log_path='./logs/', eval_freq=500, deterministic=True, render=False)

# Train the model (you can switch between PPO and MADDPG models here)
model_ppo.learn(total_timesteps=10000, callback=eval_callback)

# Once trained, adjust the environment based on agent performance
# Simulate a scenario where agent performance is high and adjust curriculum
adjusted_env = adjust_curriculum(agent_performance=0.85, difficulty_level=2)

# Train again with new environment settings
model_ppo.learn(total_timesteps=5000, callback=eval_callback)
