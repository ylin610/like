# coding: utf-8
import os
from dotenv import load_dotenv


env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)


from like import create_app
app = create_app('production')
