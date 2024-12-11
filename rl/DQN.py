from gym.game_env import CarRacingEnv

from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

# env = CarRacingEnv(render_mode="human")
env = CarRacingEnv(render_mode="rgb_array")

model = DQN(
    "MlpPolicy",
    env,
    batch_size=64,
    verbose=1
)

model.learn(total_timesteps=1_000_000)

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Mean reward: {mean_reward} +/- {std_reward}")


model.save("dqn_car_racing")