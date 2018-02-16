import os
import redis

from flask import render_template_string

def load(app):
    # If we're not using redis, then you probably messed up
    if not app.config.get('CACHE_REDIS_URL'):
        print('WARNING!!! Not using Redis. Try setting the REDIS_URL environment variable')
        redis_host = None
        redis_port = None
    else:
        redis_host, redis_port = app.config.get('CACHE_REDIS_URL').split(':')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'redis.html')

    @app.route('/admin/redis', methods=['GET'])
    def view_redis_settings():
        
        if not redis_host or not redis_port:
            error = 'REDIS_URL environment variable not set'
            redis_data = None
        else:
            try:
                client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
                redis_keys = client.keys('ctfd:*')
                redis_values = client.mget(redis_keys) 
                redis_data = dict(zip(redis_keys, redis_values))
                error = None
            except Exception as e:
                error = e
                redis_data = None

        with open(template_path) as template_file:
            template = template_file.read()
        return render_template_string(template, error=error, redis_data=redis_data)
    



