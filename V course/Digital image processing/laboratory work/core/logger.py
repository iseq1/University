"""
Класс-обработчик для настройки цветного логирования и автоматического вывода сообщений.
"""
import logging
import inspect
import sys


class CustomLogger:
    """Менеджер для цветного логирования с автоматическим определением вызова."""

    class ColorFormatter(logging.Formatter):
        """Форматтер с цветной подсветкой уровней логов."""

        class LogColors:
            """Цвета логов"""
            RESET = "\033[0m"
            RED = "\033[31m"
            GREEN = "\033[32m"
            YELLOW = "\033[33m"
            BLUE = "\033[34m"
            MAGENTA = "\033[35m"
            CYAN = "\033[36m"
            WHITE = "\033[37m"

        COLORS = {
            logging.DEBUG: LogColors.CYAN,
            logging.INFO: LogColors.GREEN,
            logging.WARNING: LogColors.YELLOW,
            logging.ERROR: LogColors.RED,
            logging.CRITICAL: LogColors.MAGENTA
        }

        def format(self, record):
            color = self.COLORS.get(record.levelno, "\033[37m")
            message = super().format(record)
            return f"{color}{message}\033[0m"

    @staticmethod
    def get_logger(name: str = "AppLogger") -> logging.Logger:
        """Получение логера"""
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            formatter = CustomLogger.ColorFormatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                "%H:%M:%S"
            )
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            logger.propagate = False
        return logger

    @staticmethod
    @staticmethod
    def auto(
        logger: logging.Logger,
        msg_map: dict,
        level: str = "info",
        status: str = "success",
        extra_msg: str = None
    ):
        """
        Автоматический логгер, который определяет имя вызывающей функции и выводит сообщение
        в зависимости от статуса ('success', 'error', 'warning').
        """
        caller = inspect.stack()[1]
        func_name = caller.function

        # --- ищем сообщение ---
        base_entry = msg_map.get(func_name)
        if isinstance(base_entry, dict):
            base_msg = base_entry.get(status, f"[{func_name}] — сообщение '{status}' не найдено.")
        else:
            base_msg = base_entry or f"[{func_name}] — сообщение не найдено в LOGGER_MSG_MAP"

        # --- дополняем ---
        full_msg = f"{base_msg} {extra_msg or ''}".strip()

        # --- выбираем метод по уровню ---
        log_func = getattr(logger, level, logger.info)
        log_func(full_msg)