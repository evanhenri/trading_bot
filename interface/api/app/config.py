class Config:
    WTF_CSRF_ENABLED = True


class Development(Config):
    ASSETS_DEBUG = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


class Production(Config):
    pass


class Testing(Development):
    TESTING = True
