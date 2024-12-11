from stable_baselines3.common.vec_env import VecFrameStack

from envs.game_env import CarRacingEnv

import time

from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

# env = CarRacingEnv(render_mode="human", no_fps_limiter=True)
env = CarRacingEnv(render_mode="rgb_array")
# env = make_vec_env(CarRacingEnv, n_envs=16, env_kwargs={"render_mode": "human", "no_fps_limiter": True})
# env = make_vec_env(CarRacingEnv, n_envs=16, env_kwargs={"render_mode": "rgb_array"})

model = DQN(
    "MlpPolicy",
    env,
    learning_rate=1e-4,
    buffer_size=200000,
    learning_starts=1000,
    batch_size=64,
    tau=0.1,
    gamma=0.98,
    train_freq=4,
    gradient_steps=1,
    exploration_fraction=0.3,
    exploration_final_eps=0.1,
    policy_kwargs=dict(
        net_arch=[256, 256],  # Two hidden layers with 256 neurons each
    ),
    verbose=1,
)

start_time = time.time()
model.learn(total_timesteps=500_000)
end_time = time.time()

training_duration = end_time - start_time
print(f"Training duration: {training_duration:.2f} seconds")

print("Saving model...")
model.save("dqn_car_racing")

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Mean reward: {mean_reward} +/- {std_reward}")

print("Simulating model...")

env = CarRacingEnv(render_mode="human")

obs, _ = env.reset()
for _ in range(10000):
    action, states = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    # env.render()
    if terminated or truncated:
        obs, _ = env.reset()
