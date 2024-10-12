import logging
import time


class LogUtils:
    def __init__(
        self,
        stage=None,
    ):
        self.stage = stage

    def _is_handler_exists(self, handler_type):
        root_logger = logging.getLogger()
        return any(isinstance(h, handler_type) for h in root_logger.handlers)

    def _get_or_create_console_handler(self):
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                return handler

        console_log_handler = logging.StreamHandler()
        root_logger.addHandler(console_log_handler)
        return console_log_handler

    def configure_logging(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)  # Set root logger level to INFO

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)
        formatter = logging.Formatter(log_format)

        if self.stage == "development":
            console_log_handler = self._get_or_create_console_handler()
            console_log_handler.setLevel(logging.INFO)
            console_log_handler.setFormatter(formatter)
        else:
            raise NotImplementedError(
                "Only development stage is supported. We can add aws cloudwatch log handler here."
            )
            # if not self._is_handler_exists(watchtower.CloudWatchLogHandler):
            #     cw_log_handler = watchtower.CloudWatchLogHandler(
            #         log_group=self.log_group_name,
            #         stream_name=self.log_stream_name,
            #         boto3_client=self.cw_logs,
            #     )
            #     cw_log_handler.setFormatter(formatter)

            #     # Add AWS CloudWatch Log Handler to the root logger
            #     root_logger.addHandler(cw_log_handler)


def log_operation(operation_name, func, exception_callback=None, *args, **kwargs):
    start_time = time.time()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting operation: {operation_name}")
    try:
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(
            f"Completed operation: {operation_name} in {elapsed_time:.2f} seconds"
        )
        return result
    except Exception as e:
        message = f"Error during operation: {operation_name} - {str(e)}"
        logger.error(
            message,
            exc_info=True,
        )
        if exception_callback:
            exception_callback(message, e)
        raise  # Re-raise the exception after logging


def log_operation_decorator(operation_name, exception_callback=None):

    def decorator(func):
        def wrapper(*args, **kwargs):

            result = log_operation(
                operation_name, func, exception_callback, *args, **kwargs
            )

            return result

        return wrapper

    return decorator
