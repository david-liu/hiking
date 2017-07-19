from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import optparse
import logging
from flask import request, jsonify

from hiking.utils.rest_helper import success_response, fail_response, error_response


logger = logging.getLogger(__name__)

class WebServiceLoader(object):
    def __init__(self, app):
        self.app = app

        app.add_url_rule('/', 'index', self.index, methods=['GET'])
        app.add_url_rule('/api/inspect', 'service_inspect', self.api_inspect, methods=['GET'])
        app.add_url_rule('/api/<noun>/<verb>', 'service', self.service, methods=['POST', 'GET'])

        self.service_registry= {}


    def get_command_line_options(self, default_host, default_port):
        """
        Takes a flask.Flask instance and runs it. Parses 
        command-line flags to configure the app.
        """

        # Set up the command-line options
        parser = optparse.OptionParser()
        parser.add_option("-H", "--host",
                          help="Hostname of the Flask app " + \
                               "[default %s]" % default_host,
                          default=default_host)
        parser.add_option("-P", "--port",
                          help="Port for the Flask app " + \
                               "[default %s]" % default_port,
                          default=default_port)

        # Two options useful for debugging purposes, but 
        # a bit dangerous so not exposed in the help message.
        parser.add_option("-d", "--debug",
                          action="store_true", dest="debug",
                          help=optparse.SUPPRESS_HELP)
        parser.add_option("-p", "--profile",
                          action="store_true", dest="profile",
                          help=optparse.SUPPRESS_HELP)

        options, _ = parser.parse_args()

        return options

    def start(self, default_host="0.0.0.0", 
                  default_port="5000"):
        logger.info("start app on %s:%s", default_host, default_port)
            
        # options = self.get_command_line_options(default_host, default_port)

        # # If the user selects the profiling option, then we need
        # # to do a little extra setup
        # if options.profile:
        #     from werkzeug.contrib.profiler import ProfilerMiddleware

        #     app.config['PROFILE'] = True
        #     app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
        #                    restrictions=[30])
        #     options.debug = True
        #     
        
        self.app.run(
            debug=False,
            host=default_host,
            port=int(default_port)
        )

    def index(self):
        return 'Hello service'

    def api_inspect(self):
        serivce_desc = {}
        for key, service_config in self.service_registry.items():
            url = '/api/' + "/".join(key.split('.'))

            parameters = {}

            for arg, config in service_config['required_args'].items():

                parameters_config = dict(config.items()[:])
                parameters_config["required"] = True
                parameters[arg] = parameters_config
                

            for arg, config in service_config['optional_args'].items():
                parameters_config = dict(config.items()[:])
                parameters_config["required"] = False
                parameters[arg] = parameters_config
            

            serivce_desc[url] = {
                'desc' : service_config['desc'],
                'parameters' :parameters
            }

        return jsonify(serivce_desc)


    def service(self, noun, verb):
        if request.method == 'POST':

            if request.json:

                service_config = self._find_service_config(noun, verb)


                if not service_config:
                    return jsonify(fail_response('there is no service registed on /api/%s/%s' % (noun, verb)))


                return self._invoke_service(request.json, service_config)

            else:
                return jsonify(error_response("can not found any data"))
        elif request.method == 'GET':
        
            service_config = self._find_service_config(noun, verb)

            if not service_config:
                return jsonify(fail_response('there is no service registed on /api/%s/%s' % (noun, verb)))

            return self._invoke_service(request.args, service_config)
            


    def _invoke_service(self, request_data, service_config):
        requested_args = service_config['required_args']
        optional_args = service_config['optional_args']

        request_payload = {}
        input_error_messages = {}
        for arg in requested_args.keys():
            if arg in request_data:
                request_payload[arg] = request_data[arg]
            else:
                input_error_messages[arg] = 'the field [%s] is required' % arg


        for arg in optional_args.keys():
            if arg in request_data:
                request_payload[arg] = request_data[arg]
        

        if input_error_messages:
            return jsonify(fail_response(input_error_messages))
        else:
            service_fn = service_config['method']
            try:
                result = service_fn(**request_payload)

                return jsonify(success_response(result))

            # except ValueError as inst:
            #     return jsonify(fail_response(str(inst)))

            except Exception as inst:
                logger.debug("find exception during evaluate: %s", inst)

                return jsonify(error_response(str(inst)))

     
        

    def register_service_object(self, obj):
        all_methods = inspect.getmembers(obj, predicate=inspect.ismethod)

        for name, method in all_methods:
            self.register_service_method(method)

    def register_service_method(self, method):
        if(hasattr(method, '__service_config__')):
            service_config = method.__service_config__

            logger.info("begin to register method: %s on [%s:%s]" % (method.__name__, service_config['noun'], service_config['verb']))
            
            
            key = "%s.%s" % (service_config['noun'], service_config['verb'])

            if key in self.service_registry:
                raise ValueError('there existed a service registered with: noun=%s, verb=%s' % (service_config['noun'], service_config['verb']))

            self.service_registry[key] = {
                'method' : method,
                'desc' : service_config['description'],
                'required_args' : service_config['required_args'],
                'optional_args' : service_config['optional_args']
            }

    def _find_service_config(self, noun, verb):
        key = "%s.%s" % (noun, verb)
        if key in self.service_registry:
            return self.service_registry[key]
        else:
            return None