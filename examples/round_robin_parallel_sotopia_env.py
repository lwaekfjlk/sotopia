import logging

from rich import print
from rich.logging import RichHandler

from sotopia.agents.llm_agent import Agents, LLMAgent
from sotopia.envs import ParallelSotopiaEnv
from sotopia.generation_utils.generate import process_history

FORMAT = "%(message)s"
logging.basicConfig(
    level="WARNING", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

env = ParallelSotopiaEnv(
    model_name="gpt-3.5-turbo", action_order="round-robin"
)
obs = env.reset()
for agent_name in env.agents:
    print(f"Here's {agent_name}'s initial observation\n{obs[agent_name]}")
agents = Agents()
for agent_name in env.agents:
    agents[agent_name] = LLMAgent(agent_name)

agents.reset()
done = False
while not done:
    actions = agents.act(obs)
    print(actions)
    obs, _, terminated, ___, ____ = env.step(actions)
    done = all(terminated.values())