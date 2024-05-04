from oshandler import OSHandler
import logging
from abc import ABC, abstractmethod


class Logger(ABC):

    # Chat History
    # Errors
    # Experiment Runs

    # Log Structure:
    # logs
    #
    # -chat_history
    # --FrozenLake-v1
    # ---gpt-4-turbo
    # ----chat_history_1.log
    # -----Time, Role, Content
    #
    # -errors
    # --FrozenLake-v1
    # ---map
    # ----29_04_2024
    # -----map_errors_1.log
    # -----Time, Error, Message, Class, Method
    # ---language_model
    # ----gpt-4
    # -----29_04_2024
    # ------lm_errors_1.log
    # -------Time, Error, Message, Class, Method
    # ---os
    # ----29_04_2024
    # -----os_errors_1.log
    # ------Time, Error, Message, Class, Method
    # ---evaluation
    # ----29.04.2024
    # -----eval_errors_1.log
    # ------Time, Error, Message, EvaluationStep, Class, Method
    #
    # -experiments
    # --FrozenLake-v1
    # ---experiment_report_1.log
    # ----Time, Strategy, kShot, Map, Successful, WithErrors, EvalCreated, ErrorsLogs, ChatHistoryLogs

    @property
    def logs_dir(self) -> str:
        ...

    @property
    def log_name(self) -> str:
        ...

    @classmethod
    @abstractmethod
    def log(cls, source, content, to_logs=True) -> None:
        ...

    @classmethod
    @abstractmethod
    def flush_logs(cls) -> None:
        ...
