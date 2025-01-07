from envs.game_env import CarRacingEnv

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

# env = CarRacingEnv(render_mode="human")
# env = CarRacingEnv(render_mode="rgb_array")
# env = make_vec_env(CarRacingEnv, n_envs=16, env_kwargs={"render_mode": "human", "no_fps_limiter": True})
env = make_vec_env(CarRacingEnv, n_envs=16, env_kwargs={"render_mode": "rgb_array"})

model = PPO(
    "MlpPolicy",
    env,
    n_steps=2048,
    batch_size=512,
    n_epochs=4,
    gamma=0.97,
    gae_lambda=0.98,
    ent_coef=0.01,
    verbose=1,
    tensorboard_log="./ppo_tensorboard/"
)

model.learn(total_timesteps=15_000_000)

print("Saving model...")
model.save("ppo_car_racing")

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Mean reward: {mean_reward} +/- {std_reward}")

env = CarRacingEnv(render_mode="human")

obs, _ = env.reset()
for _ in range(10000):
    action, states = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    # env.render()
    if terminated or truncated:
        obs, _ = env.reset()
