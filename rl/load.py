from gym.game_env import CarRacingEnv
from stable_baselines3 import PPO, DQN

env = CarRacingEnv(render_mode="human")
model = DQN.load("rl/dqn_car_racing.zip")

obs, _ = env.reset()
for _ in range(10000):
    action, states = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated or truncated:
        obs, _ = env.reset()

env.close()