from flask import Flask, render_template, request
from sqlalchemy import desc
from sqlalchemy.orm import Session

from config.config import configuration_data
from database.models import Inventory, Location, Product, engine
from processing_request.processing_request import (
    processing_request_add_location,
    processing_request_add_product,
    processing_request_add_product_to_inventory,
    processing_request_change_quantity,
    processing_request_del_product_from_inventory,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = configuration_data.secret_key.get_secret_value()
app.config['DEBUG'] = configuration_data.debug


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.form)
    mod_search = False
    mode_sorting = False
    if request.method == 'POST' and request:
        if set(['search_word']) == set(request.form.keys()):
            mod_search = True
            search_text = request.form.get('search_word')
        if set(['sort']) == set(request.form.keys()):
            mode_sorting = True

        if set(['new_quantity', 'inventory_id']) == set(request.form.keys()):
            processing_request_change_quantity(request.form)

        if set(['inventory_id']) == set(request.form.keys()):
            processing_request_del_product_from_inventory(request.form)

        if set(['location_id', 'quantity', 'product_id']) == set(
            request.form.keys()
        ):
            processing_request_add_product_to_inventory(request.form)
        if set(
            ['product_name', 'product_description', 'product_price']
        ) == set(request.form.keys()):
            processing_request_add_product(request.form)
        if 'location' in request.form.keys():
            processing_request_add_location((request.form))

    template = 'index.html'
    title = 'Таблица с информацией о товарах'

    if mod_search:
        inventory = (
            Session(autoflush=False, bind=engine)
            .query(Inventory)
            .join(Product)
            .filter(Product.name.like(f'%{search_text}%'))
            .all()
        )

    elif mode_sorting and int(request.form.get('sort')) == 1:
        inventory = (
            Session(autoflush=False, bind=engine)
            .query(Inventory)
            .join(Product)
            .order_by(Product.price)
            .all()
        )

    elif mode_sorting and int(request.form.get('sort')) == 2:
        inventory = (
            Session(autoflush=False, bind=engine)
            .query(Inventory)
            .join(Product)
            .order_by(desc(Product.price))
            .all()
        )

    else:
        inventory = (
            Session(autoflush=False, bind=engine).query(Inventory).all()
        )

    context = {
        'title': title,
        'inventory': inventory,
        'product': (
            Session(autoflush=False, bind=engine).query(Product).all()
        ),
        'location': (
            Session(autoflush=False, bind=engine).query(Location).all()
        ),
    }

    return render_template(template, context=context)


if __name__ == '__main__':
    app.run()
