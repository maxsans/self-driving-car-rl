from envs.game_env import CarRacingEnv
from stable_baselines3 import PPO

env = CarRacingEnv(render_mode="human", versus=True)

# model = PPO.load("rl/ppo_car_racing.zip")
model = PPO.load("all-models/ppo_car_racing-5-75000000_steps")

obs, _ = env.reset()
for _ in range(10000):
    action, states = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    # env.render()
    if terminated or truncated:
        obs, _ = env.reset()

env.close()
