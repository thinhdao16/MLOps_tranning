from .index_route import index_bp
from .predict_route import predict_bp

def register_routes(app):
    # Đăng ký các blueprint
    app.register_blueprint(index_bp)
    app.register_blueprint(predict_bp)