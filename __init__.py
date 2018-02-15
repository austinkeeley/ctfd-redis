import os
import redis

from flask import render_template_string

def load(app):
    # If we're not using redis, then you probably messed up
    if not app.config.get('CACHE_REDIS_URL'):
        print('WARNING!!! Not using Redis. Try setting the REDIS_URL environment variable')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'redis.html')

    @app.route('/admin/redis', methods=['GET'])
    def view_redis_settings():
        
        if not app.config.get('CACHE_REDIS_URL'):
            error = 'REDIS_URL environment variable not set'
        else:
            # Attempt a connection to the redis server
            client = redis.from_url('redis://%s' % (app.config['CACHE_REDIS_URL']))
            client.set('ctfd:test_key', 'test_value')
            response = client.get('ctfd:test_key')
            if response != b'test_value':
                error = 'Could not connect to Redis'
            else:
                error = None

        with open(template_path) as template_file:
            template = template_file.read()
        return render_template_string(template, config=app.config, error=error)
    



