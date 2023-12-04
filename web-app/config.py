class Config(object):
    """基础配置类"""
    SECRET_KEY = 'your_secret_key'
    DEBUG = False
    MONGO_URI = 'your_production_mongo_uri'


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/Isomorphism'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    MONGO_URI = 'your_testing_mongo_uri'


class ProductionConfig(Config):
    """生产环境配置"""
    MONGO_URI = 'your_production_mongo_uri'
