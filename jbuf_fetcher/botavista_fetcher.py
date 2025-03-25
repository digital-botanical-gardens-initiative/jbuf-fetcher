import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

project_dict_str = os.getenv("PROJECT")