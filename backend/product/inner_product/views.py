from flask import Blueprint

products = Blueprint('product', __name__)


@products.route('/', methods=['GET'])
def index():
    return 'this index page'
