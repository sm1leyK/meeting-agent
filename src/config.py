#config.py
import os
from pathlib import Path
from dotenv import load_dotenv

#加在 .env文件
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    '''应用配置'''
    
    #API keys
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    
    #应用配置
    APP_ENV = os.getenv('APP_ENV','development')
    LOG_LEVEL = os.getenv('LOG_LEVEL','INFO')
    DEBUG = os.getenv('DEBUG','false').lower() == 'true'
    
    @classmethod
    def validate(cls):
        '''验证必要配置'''
        missing = []
        if not cls.DEEPSEEK_API_KEY:
            missing.append('DEEPSEEK_API_KEY')
        if missing:
            raise ValueError(f"缺少必要的环境变量: {', '.join(missing)}")
        


