from flask import Flask, request, render_template
import jwt
import random
import datetime
from dateutil.relativedelta import relativedelta

# EXPORTS FUNCTIONS START
from main.auth import token_required
from main.user.models.user_model import User
from main.user.controllers.order_controller import get_user_orders, get_order_by_id, track_order
from main.user.controllers.product_controller import (
get_product_by_id, 
get_popular_tags, 
get_popular_variants, 
get_search_products, 
get_all_products,
get_user_reviews,
get_all_reviews, 
get_other_products, 
get_related_products )
from main.user.models.user_model import User
from main.user.controllers.order_controller import get_cart
from main.user.controllers.blog_controller import get_blogs, get_blog_tags, get_blog_by_id, get_other_blog_categories, get_related_blog_categories

app = Flask(__name__, static_url_path='/static', static_folder='../../web/static', template_folder='../../web/templates')
app.config.from_pyfile("config/config.cfg")





  # Index Route
def home():
    one_month_ago = datetime.datetime.now() - relativedelta(months=1)
    
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    token = request.cookies.get('token')
    cart = get_cart()
    # get all products reviews
    reviews = get_all_reviews()
    
    # for all products
    page_num = request.args.get('page_num', default=1)
    product_name = request.args.get('product_name', default=None)
    product_tag = request.args.get('product_tag', default=None)
    min_price = request.args.get('min', default=1)
    max_price = request.args.get('max', default=99999999)
    products = get_all_products()
    
    if not token:  # Token doesn't exist
        return render_template('user/index.html', cart=cart, messageError=message_error, message=message, all_reviews=reviews, products=products, one_month_ago=one_month_ago)
    else:
        try:
            # Decode the token and fetch the user
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.collection.find_one({'email': data['email']})
            if not current_user:
                raise Exception("User not found")
        except Exception as e:
            return render_template('user/login.html')

        # Render the page with the current user's details
        return render_template('user/index.html', user=current_user, cart=cart, messageError=message_error, message=message, all_reviews=reviews, products=products, one_month_ago=one_month_ago)
    
    
  # dashboard normal user/ Buyer
@token_required
def user_dashboard(current_user):
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    cart = get_cart()
    user_orders = get_user_orders(current_user['_id'])
    return render_template('user/dashboard.html', cart=cart, user=current_user, orders=user_orders,  messageError=message_error, message=message)
  
   
  # orders page for user
@token_required
def orders(current_user): 
    tracking_no = request.args.get('tracking_no')
    tracked_order = track_order(tracking_no)
    cart = get_cart()
    user_orders = get_user_orders(current_user['_id'])
    return render_template('user/orders.html', user=current_user, cart=cart, orders=user_orders, tracking=tracked_order)
  
  
  # checkout page
@token_required
def checkout(current_user): 
    cart = get_cart()
    order_id = request.args.get('order_id')
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    user_orders = get_order_by_id(order_id)
    return render_template('user/checkout.html', user=current_user, cart=cart, orders=user_orders,  messageError=message_error, message=message)
  
  
# product single detail page
def product_detail(product_id): 
    token = request.cookies.get('token')
    
     # get the cart information
    cart = get_cart()
    # the page number on the product for the reviews
    page_num = request.args.get('page_num', default=1)
    # message args for the return messages
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    # product id to get a single product info
    product = get_product_by_id(product_id)
    # get other products that are related and not-related
    relatedProducts = get_related_products(product_id)
    otherProducts = get_other_products(product_id)
    # get the user reviews and it's pages
    userReviews = get_user_reviews(product_id, page_num)[0]
    all_reviews = get_all_reviews()
    userReviews_pages = get_user_reviews(product_id, page_num)[1]
    
    # calculate the ratings for current single product
    ratings = [int(rating['rating']) for rating in userReviews]
    total_rating = sum(ratings)
    review_count = len(ratings)
    averagerating = (total_rating / review_count) if review_count > 0 else 0
    
    if not token:  # Token doesn't exist
        return render_template('user/product.html', cart=cart, 
                              reviews=userReviews, 
                              all_reviews=all_reviews,
                              reviews_pages=userReviews_pages, 
                              rating=averagerating,
                              product=product, 
                              relatedProducts=relatedProducts, 
                              otherProducts=otherProducts,  
                              messageError=message_error, 
                              message=message )
    else:
      try:
        # Decode the token and fetch the user
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.collection.find_one({'email': data['email']})
        if not current_user:
            return render_template('user/login.html')
            
          
       
        return render_template('user/product.html', cart=cart, 
                              user=current_user, 
                              reviews=userReviews, 
                              all_reviews=all_reviews,
                              reviews_pages=userReviews_pages, 
                              rating=averagerating,
                              product=product, 
                              relatedProducts=relatedProducts, 
                              otherProducts=otherProducts,  
                              messageError=message_error, 
                              message=message )
      except Exception as e:
        return {"message": "Internal server error"}, 500
        
        
      
  # shop page for good list
def catalog():
      cart = get_cart() # products in cart
      tags = get_popular_tags() # popular tags list
      variants = get_popular_variants() # popular variants list
      
      # get all reviews
      reviews = get_all_reviews()
      
      
      # display products in catalog with filter
      page_num = request.args.get('page_num', default=1)
      product_name = request.args.get('product_name', default=None)
      product_tag = request.args.get('product_tag', default=None)
      min_price = request.args.get('min', default=1)
      max_price = request.args.get('max', default=99999999)
      searched_products = get_search_products(product_name, product_tag, min_price, max_price, page_num)[0]
      random.shuffle(searched_products)
      searched_pages = get_search_products(product_name, product_tag, min_price, max_price, page_num)[1]
      
      
      return render_template('user/shop.html', cart=cart, 
                             show_login="no", 
                             tags=tags, 
                             all_reviews=reviews,
                             variants=variants, 
                             searched_products=searched_products, 
                             searched_pages=searched_pages )
    
    
  
  
  # create a new user account
def signup():
    return render_template('user/signup.html', show_cart="no")
  
  
  # login page
def login():
    return render_template('user/login.html', show_cart="no")
  
  # update password
@token_required
def change_password(current_user):
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    cart = get_cart()
    return render_template('user/change_password.html', user=current_user, cart=cart, messageError=message_error, message=message)
   
  # update user profile
@token_required
def change_profile(current_user):
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    cart = get_cart()
    return render_template('user/update_profile.html', user=current_user, cart=cart, messageError=message_error, message=message, delete_="yes")

# URL for blogs
def blog():
  page_num = request.args.get('page_num', default=1)
  cat = request.args.get('cat', default="all")
  blogs = get_blogs(page_num, cat)[0]
  total_pages = get_blogs(page_num, cat)[1]
  blog_tags = get_blog_tags()
  return render_template('user/blog.html', blogs=blogs, tags=blog_tags, total_pages=total_pages)
 
# URL for blog post detail
def blog_post(blog_id):
  single_blog_post = get_blog_by_id(blog_id)
  other_blogs = get_other_blog_categories(blog_id)
  related_blogs = get_related_blog_categories(blog_id)
  return render_template('user/blog_post.html', single_blog=single_blog_post, other_blogs=other_blogs, related_blogs=related_blogs)


def post():
  return render_template('user/add_post.html')


# URL for payments
def payment_success():
   return render_template('user/paysuccess.html')
  
  
def payment_failed():
    return render_template('user/payfailed.html')
  
def about_us():  # terms and conditions page
    cart = get_cart()
    return render_template('user/about.html', cart=cart)
  
def contact_us():  # terms and conditions page
    cart = get_cart()
    return render_template('user/contact.html', cart=cart)
  
def faqs():  # terms and conditions page
    return render_template('user/faqs.html') 
  
def policy():  # policy page
    return render_template('user/policy.html')
  
  
def terms_condition():  # terms and conditions page
    return render_template('user/terms-condition.html')

def view_sitemap():
    return render_template('user/sitemap.xml')
  
def robots_txt():
    return render_template('user/robots.txt')
  
  
  
  

    
    
    
    