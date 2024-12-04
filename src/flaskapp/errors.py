from flask import jsonify

def register_error_handlers(app):

    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': error.code, 'message': error.name, 'detail': error.description}), 400
    
    @app.errorhandler(401)
    def not_found_error(error):
        return jsonify({'error': error.code, 'message': error.name, 'detail': error.description}), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({'error': error.code, 'message': error.name, 'detail': error.description}), 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': error.code, 'message': error.name, 'detail': error.description}), 404
    