import logging
import os
from datetime import datetime


FORMAT = "[%(asctime)s] %(levelname)s | {%(message)s}"
DIR_PATH = os.path.join(os.getcwd(), "logs")
FILE_NAME = f"{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.log"
FILE_PATH = os.path.join(DIR_PATH, FILE_NAME)

os.makedirs(DIR_PATH, exist_ok=True)


logging.basicConfig(filename=FILE_PATH, format=FORMAT, level=logging.INFO)
