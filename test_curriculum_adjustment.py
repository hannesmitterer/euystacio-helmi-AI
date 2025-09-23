from multi_agent_rl_curriculum import DynamicMultiAgentEnv, adjust_curriculum

env = DynamicMultiAgentEnv()
difficulty_level = 1

# Simulate agent performing well
agent_performance = 0.9
env = adjust_curriculum(agent_performance, difficulty_level)
print("Adjusted Action Space:", env.action_space)
print("Adjusted Observation Space:", env.observation_space)