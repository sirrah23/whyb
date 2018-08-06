class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "super-secret"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site_prod.db'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site_dev.db'
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site_test.db'
    TESTING = True


def getConfigObject(cfg_type):
    cfg_map = {
        'production'  : ProductionConfig,
        'development' : DevelopmentConfig,
        'testing'     : TestingConfig,
    }
    return cfg_map.get(cfg_type.lower(), Config)
