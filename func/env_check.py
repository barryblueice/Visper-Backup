import os,loguru
from dotenv import load_dotenv

def initial_env():
    env_variables = {
        'SOURCE_PATH': '',
        'TARGET_PATH': '',
        'TIME': '5',
        'WEBPORT': '5555'
    }

    with open(os.path.join(os.getcwd(),'.env'), 'w') as file:
        for key, value in env_variables.items():
            file.write(f'{key}={value}\n')

def get_env():
    load_dotenv()
    source_path = os.getenv('SOURCE_PATH')
    target_backup_path = os.getenv('TARGET_PATH')
    keeptime = os.getenv('TIME')
    webport = os.getenv('WEBPORT')
    return source_path,target_backup_path,keeptime,webport