"""
Файл содержит реализацию экспериментов в контексте задачи об многоруком бандите
"""
from plugins import BanditEnv, GreedyAlgorithm, EpsilonGreedyAlgorithm, UCBAlgorithm, GradientAlgorithm
from utils import run_multiple_experiments, logger, plot_parameter_results, plot_levers_diff, plot_algorithms_diff_results


class BanditAlgorithmResearch:
    """Класс, описывающий эксперименты в контексте задачи об многоруком бандите"""


    CONFIG = {
        "Greedy": {
            "pipeline": lambda env, empty_param: GreedyAlgorithm(
                n_actions=env.n_actions,
                empty_param=empty_param
            ),
            "base_param": None,
        },
        "Epsilon-Greedy": {
            "pipeline": lambda env, epsilon: EpsilonGreedyAlgorithm(
                n_actions=env.n_actions,
                epsilon=epsilon
            ),
            "base_param": 0.5
        },
        "UCB": {
            "pipeline": lambda env, c_value: UCBAlgorithm(
                n_actions=env.n_actions,
                c=c_value
            ),
            "base_param": 1.0
        },
        "Gradient": {
            "pipeline": lambda env, alpha: GradientAlgorithm(
                n_actions=env.n_actions,
                alpha=alpha
            ),
            "base_param": 0.1
        }
    }


    def __init__(self, bandit_env: BanditEnv = None, payout_list: list[int] = None, reward_list: list[int] = None):
        """Инициализация класса и его внутреннего состояния"""

        if bandit_env:
            self.env = bandit_env
        elif payout_list and reward_list:
            self.env = BanditEnv(payout_list=payout_list, reward_list=reward_list)
        else:
            self.env = BanditEnv()


    def algorithms_diff_experiment(self, n_episodes=10_000, n_runs=100):
        """Эксперимент: сравнение результатов разных алгоритмов"""
        all_results = {}

        for name, algorithm_info in self.CONFIG.items():
            algorithm_factory, parameter = algorithm_info["pipeline"], algorithm_info["base_param"]
            logger.info(f"Запуск {name}: базовый параметр = %s", parameter)

            all_results[name] = run_multiple_experiments(
                env=self.env,
                algorithm_factory=lambda factory=algorithm_factory, env=self.env, param=parameter: factory(env, param),
                n_episodes=n_episodes,
                n_runs=n_runs
            )

        for name, result in all_results.items():
            logger.info(
                f"{name}:\n"
                f"reward = {result['average_rewards'][-1]:.4f},\n"
                f"optimal = {result['optimal_action_rate'][-1]:.4f}\n"
            )

        plot_algorithms_diff_results(
            baseline_results=all_results,
            save_path="plots/algorithms_diff/"
        )


    def epsilon_greedy_experiment(self, n_episodes: int = 10_000, n_runs: int = 100, config_name: str = "Epsilon-Greedy"):
        """Эксперимент: сравнение результатов эпсилон-жадного алгоритма с разным значением epsilon"""
        algorithm_factory = self.CONFIG[config_name]["pipeline"]
        epsilon_values = [0.01, 0.05, 0.1, 0.2, 0.5]

        epsilon_results = {}

        for epsilon in epsilon_values:
            logger.info(f"Запуск {config_name}: epsilon = %s", epsilon)

            epsilon_results[epsilon] = run_multiple_experiments(
                env=self.env,
                algorithm_factory=lambda factory=algorithm_factory, env=self.env, e=epsilon: factory(env, e),
                n_episodes=n_episodes,
                n_runs=n_runs
            )

        for epsilon, result in epsilon_results.items():
            logger.info(
                f"epsilon = {epsilon}:\n"
                f"reward = {result['average_rewards'][-1]:.4f},\n"
                f"optimal = {result['optimal_action_rate'][-1]:.4f}\n"
            )

        plot_parameter_results(
            parameter_values=epsilon_values,
            results=epsilon_results,
            parameter_name='epsilon',
            title=config_name,
            save_path='plots/epsilon/'
        )


    def ucb_experiment(self, n_episodes: int = 10_000, n_runs: int = 100, config_name: str = "UCB"):
        """Эксперимент: сравнение результатов алгоритма верхней доверительной границы с разным значением C"""
        algorithm_factory = self.CONFIG[config_name]["pipeline"]
        c_values = [0.1, 0.5, 1.0, 2.0, 5.0]

        c_results = {}

        for c_value in c_values:
            logger.info(f"Запуск {config_name}: c_value = %s", c_value)


            c_results[c_value] = run_multiple_experiments(
                env=self.env,
                algorithm_factory=lambda factory=algorithm_factory, env=self.env, c=c_value: factory(env, c),
                n_episodes=n_episodes,
                n_runs=n_runs
            )

        for c, result in c_results.items():
            logger.info(
                f"c = {c}:\n"
                f"reward = {result['average_rewards'][-1]:.4f},\n"
                f"optimal = {result['optimal_action_rate'][-1]:.4f}\n"
            )

        plot_parameter_results(
            parameter_values=c_values,
            results=c_results,
            parameter_name='c_value',
            title=config_name,
            save_path='plots/ucb/'
        )


    def gradient_experiment(self, n_episodes: int = 10_000, n_runs: int = 100, config_name: str = "Gradient"):
        """Эксперимент: сравнение результатов градиентного алгоритма с разным значением alpha"""
        algorithm_factory = self.CONFIG[config_name]["pipeline"]
        alpha_values = [0.01, 0.05, 0.1, 0.5, 1.0]

        alpha_results = {}

        for alpha in alpha_values:
            logger.info(f"Запуск {config_name}: alpha = %s", alpha)

            alpha_results[alpha] = run_multiple_experiments(
                env=self.env,
                algorithm_factory=lambda factory=algorithm_factory, env=self.env, a=alpha: factory(env, a),
                n_episodes=n_episodes,
                n_runs=n_runs
            )

        for alpha, result in alpha_results.items():
            logger.info(
                f"alpha = {alpha}: \n"
                f"reward = {result['average_rewards'][-1]:.4f}, \n"
                f"optimal = {result['optimal_action_rate'][-1]:.4f}\n"
            )

        plot_parameter_results(
            parameter_values=alpha_values,
            results=alpha_results,
            parameter_name='alpha',
            title=config_name,
            save_path='plots/gradient/'
        )


    def count_lever_experiment(self, n_episodes: int = 10_000, n_runs: int = 100) -> dict:
        """Эксперимент: сравнение результатов с разным количеством рычагов на качество работы алгоритмов"""

        levers_list = [3, 5, 10, 20]
        action_count_results = {}

        for n_actions in levers_list:
            logger.info("Количество рычагов: %s", n_actions)

            env_current = BanditEnv(n_lever=n_actions)

            action_count_results[n_actions] = {}

            for algorithm_name, algorithm_info in self.CONFIG.items():
                logger.info("Запуск: %s", algorithm_name)

                algorithm_factory = algorithm_info["pipeline"]
                algorithm_parameter = algorithm_info["base_param"]

                action_count_results[n_actions][algorithm_name] = (
                    run_multiple_experiments(
                        env=env_current,
                        algorithm_factory=lambda factory=algorithm_factory, env=env_current, param=algorithm_parameter: factory(env, param),
                        n_episodes=n_episodes,
                        n_runs=n_runs
                    )
                )

        for n_actions in action_count_results:
            logger.info("%s рычагов\n", n_actions)

            for algorithm_name in action_count_results[n_actions]:
                result = action_count_results[n_actions][algorithm_name]

                logger.info(
                    f"{algorithm_name}: \n"
                    f"reward = {result['average_rewards'][-1]:.4f}, \n"
                    f"optimal = {result['optimal_action_rate'][-1]:.4f}\n"
                )

        plot_levers_diff(
            levers_list=levers_list,
            action_count_results=action_count_results,
            save_path="plots/levers_diff/"
        )

        return action_count_results


    def get_research(self, n_episodes=10_000, n_runs=100):
        """Провести все эксперименты"""
        self.algorithms_diff_experiment(n_episodes=n_episodes, n_runs=n_runs)
        self.epsilon_greedy_experiment(n_episodes=n_episodes, n_runs=n_runs)
        self.ucb_experiment(n_episodes=n_episodes, n_runs=n_runs)
        self.gradient_experiment(n_episodes=n_episodes, n_runs=n_runs)
        self.count_lever_experiment(n_episodes=n_episodes, n_runs=n_runs)
