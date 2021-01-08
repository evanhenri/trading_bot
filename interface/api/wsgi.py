def application(environ, start_response):
    from app import create_app
    app = create_app('production')
    # app = create_app('development')
    return app(environ, start_response)
