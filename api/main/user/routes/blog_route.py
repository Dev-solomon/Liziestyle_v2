from flask import Blueprint
from flask import current_app as app, render_template
from flask import request 
from main.auth import token_required
from main.user.controllers.blog_controller import *
from flask_ckeditor.utils import cleanify

blog_blueprint = Blueprint("blog",  __name__, "api/blogs")

@blog_blueprint.route('/', methods=['GET'])
def all_blogs():
    if request.method == 'GET':
       all = get_blogs()
       if all != []:
           return jsonify({
               "Message": "Fetched all blog posts."
           })
    
@blog_blueprint.route('/create', methods=['POST'])
def create_blog():
    if request.method == 'POST':
        data = request.get_json()
        # print(data)
        new_blog = create_blog_post(data) 
        if new_blog == True:
            return "Nuovo post del blog creato con successo!"
        # return data
        return "Something Went Wrong"
            

@blog_blueprint.route('/<id>', methods=['DELETE'])
@token_required
def category_by_id(current_user, id):
    if request.method == 'DELETE':
        return delete_blog_post(id)



