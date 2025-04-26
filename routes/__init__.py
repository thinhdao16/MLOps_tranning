from .index_route import index_bp
from .predict_route import predict_bp
from .rainfall_route import rainfall_bp
from .storm_route import storm_bp
from .sunny import sunny_bp
from .uv_route import uv_bp
from .visibility_route import visibility_bp

def register_routes(app):
    
    app.register_blueprint(index_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(rainfall_bp)
    app.register_blueprint(storm_bp)
    app.register_blueprint(sunny_bp)
    app.register_blueprint(uv_bp)
    app.register_blueprint(visibility_bp)