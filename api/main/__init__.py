from flask import Flask, request, render_template, session, make_response, redirect, url_for
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import os
import random
from flask_caching import Cache
import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.utils import import_string, cached_property
from jinja2 import TemplateError

class LazyView(object):

    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name) 

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)



def create_app():

  # Flask Config
  app = Flask(__name__, static_url_path='/static', static_folder='../../web/static', template_folder='../../web/templates')
  app.config.from_pyfile("config/config.cfg")
  cors = CORS(app, resources={r"/*": { "origins": app.config["FRONTEND_DOMAIN"] }})
  # Assuming you've initialized your Flask app with Flask-Caching
  cache = Cache(config={'CACHE_TYPE': 'simple'})
  cache.init_app(app)
  


  # Misc Config
  os.environ["TZ"] = app.config["TIMEZONE"]

  # Database Config
  if app.config["ENVIRONMENT"] == "production":
    mongo = MongoClient(app.config["MONGO_URI"])
    # mongo = MongoClient(app.config["MONGO_DB"], app.config["MONGO_PORT"])
  else:
    mongo = MongoClient(app.config["MONGO_URI"])
    
      # Import Routes
  with app.app_context():
    
    
    # EXPORTS FUNCTIONS END
    
    # blueprints for user routes
    from main.user.routes.user_route import user_blueprint
    from main.user.routes.product_route import product_blueprint
    from main.user.routes.category_route import category_blueprint
    from main.user.routes.order_route import order_blueprint
    from main.user.routes.blog_route import blog_blueprint
    # blueprints for seller below
    from main.seller.routes.seller_route import seller_blueprint
    

    # Register User Blueprints
    app.register_blueprint(user_blueprint, url_prefix="/api/user")
    app.register_blueprint(product_blueprint, url_prefix="/api/products")
    app.register_blueprint(category_blueprint, url_prefix="/api/categories")
    app.register_blueprint(order_blueprint, url_prefix="/api/orders")
    app.register_blueprint(blog_blueprint, url_prefix="/api/blogs")
    # Register Seller Blueprints
    app.register_blueprint(seller_blueprint, url_prefix="/api/sellers")
    
    # LazyView routes
    lazy_routes = {
        "/": "main.views.home",
        "/dashboard": "main.views.user_dashboard",
        "/orders": "main.views.orders",
        "/checkout": "main.views.checkout",
        "/product_detail/<string:product_id>": "main.views.product_detail",
        "/catalog": "main.views.catalog",
        "/signup": "main.views.signup",
        "/login": "main.views.login",
        "/update-password": "main.views.change_password",
        "/update-profile": "main.views.change_profile",
        "/paymentSuccess": "main.views.payment_success",
        "/paymentFailed": "main.views.payment_failed",
        "/about-us": "main.views.about_us",
        "/contact-us": "main.views.contact_us",
        "/faqs": "main.views.faqs",
        "/policy": "main.views.policy",
        "/blogs": "main.views.blog",
        "/blog_post/<string:blog_id>": "main.views.blog_post",
        "/add_post": "main.views.post",
        "/terms-conditions": "main.views.terms_condition",
        "/clear_cache": "main.views.clear_cache",
        "/sitemap": "main.views.view_sitemap",
        "/robots": "main.views.robots_txt",
    }
  
  
   # Custom shuffle filter for Jinja
  @app.template_filter('shuffle')
  def shuffle_list(value):
        if isinstance(value, list):
            random.shuffle(value)
        return value
      
  # Routes for App Errors
  @app.errorhandler(TemplateError)
  def handle_jinja_error(error):
    return render_template('user/400.html')
  
  @app.errorhandler(404)
  def not_found(error):
    return render_template('user/404.html')
  
  @app.errorhandler(400)
  def bad_request(error):
    return render_template('user/400.html')
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return render_template('user/500.html')
  
  
  # Register routes with LazyView
  for route, view in lazy_routes.items():
    app.add_url_rule(route, view_func=LazyView(view))






  
  return app