from research import BanditAlgorithmResearch
from plugins import BanditEnv


if __name__ == "__main__":

    research_obj = BanditAlgorithmResearch(
        bandit_env=BanditEnv(
            n_lever=3
        )
    )

    n_episodes = 10_000
    n_runs = 100

    research_obj.get_research(
        n_episodes=n_episodes,
        n_runs=n_runs
    )
