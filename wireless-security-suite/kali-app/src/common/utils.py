import logging
import subprocess


def setup_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def run_command(command: list[str], capture_output: bool = True) -> tuple[int, str, str]:
    try:
        process = subprocess.run(command, capture_output=capture_output, text=True, check=False)
        return process.returncode, process.stdout.strip(), process.stderr.strip()
    except FileNotFoundError:
        return 1, "", f"command not found: {command[0]}"
