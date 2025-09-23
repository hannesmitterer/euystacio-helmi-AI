from multi_agent_rl_curriculum import DynamicMultiAgentEnv

env = DynamicMultiAgentEnv()
obs = env.reset()
print("Initial observation:", obs)

# Simulate an agent action
action = [0, 0]  # Both agents select the same action for max reward
obs, reward, done, info = env.step(action)
print("After step - obs:", obs, "reward:", reward, "done:", done)
env.render()