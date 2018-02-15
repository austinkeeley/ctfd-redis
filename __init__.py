import os

from flask import render_template_string

def load(app):
    # If we're not using redis, then you probably messed up
    if not app.config.get('CACHE_REDIS_URL'):
        print('WARNING!!! Not using Redis. Try setting the REDIS_URL environment variable')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'redis.html')

    @app.route('/admin/redis', methods=['GET'])
    def view_redis_settings():
        with open(template_path) as template_file:
            template = template_file.read()
        return render_template_string(template, config=app.config)
    



