from logging.config import dictConfig
from typing import List

from flask import Flask, render_template, request, session, url_for, flash, jsonify
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename, redirect
from wtforms import Form, StringField, IntegerField, validators, BooleanField

from data import create_df, process_df
from db import DBSession, MineOrder


class OrderForm(Form):
    mine_name = StringField(label='矿名', name='mine_name', validators=[validators.Length(min=1, max=10)])
    price = IntegerField(label='价格', name='price', validators=[validators.NumberRange(1)])
    volume = IntegerField(label='体积', name='volume', validators=[validators.NumberRange(1)])
    is_ice = BooleanField(label='是否冰矿', name='is_ice', validators=[])


# https://docs.python.org/3/library/logging.html#levels
dictConfig({
    'version': 1,
    'root': {
        'level': 'NOTSET',
    }
})

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 10


# 日志写入文件
# root_logger = logging.getLogger()
# file_handler = logging.FileHandler('app.log')
# root_logger.addHandler(file_handler)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/order_insert", methods=['GET', 'POST'])
def insert_order():
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        db_session = DBSession()
        order = MineOrder()
        order.mine_name = form.mine_name.data
        order.price = form.price.data
        order.volume = form.volume.data
        order.is_ice = form.is_ice.data
        app.logger.info(order)
        db_session.add(order)
        db_session.commit()
        flash('订单插入成功')
        # return redirect(url_for('index'))
        form = OrderForm()
    return render_template('order_insert.html', form=form)


@app.route('/insert_test')
def insert_test():
    list_ = [
        ("黑闪冰", 53974819, 107000, True),
        ("黑闪冰2", 185515469, 402000, True),
        ("富清冰", 35626091, 119000, True),
        ("加里多斯冰", 3610317, 8000, True),
        #     ("电冰体",28624285,60000,True),
        ("电冰体", 135554071, 283000, True),
        ("电冰体2", 27405283, 61000, True),
        #     ("朱砂", 45971048, 63240,False),
        ("朱砂", 87232348, 131780, False),
        ("盈朱砂", 100000000, 122750, False),
        ("铈铌钙钛矿", 119503380, 146470, False),
        ("丰菱镉矿", 18467892, 39850, False),
        ("硅铍钇矿", 17635189, 25080, False),
        ("硅铍钇矿2", 137343922, 228840, False),
        ("丰砷铂矿", 4350425, 9040, False),
        ("丰钒铅矿", 78206816, 171040, False),
        ("富沸石", 50000000, 235110, False),
        ("铈铌钙钛矿2", 105178930, 135460, False),
        ("裕铈铌钙钛矿", 103665478, 116900, False),
    ]
    orders = [MineOrder(mine_name=t[0], price=t[1], volume=t[2], is_ice=t[3]) for t in list_]
    db_session = DBSession()
    db_session.add_all(orders)
    db_session.commit()
    return 'insert test success'


@app.route("/order_list")
def order_list():
    db_session = DBSession()
    order__all: [MineOrder] = db_session.query(MineOrder).all()
    # app.logger.info(order__all)
    return jsonify([
        {
            'id': o.order_id,
            'mine_name': o.mine_name,
            'price': o.price,
            'volume': o.volume,
            'is_ice': o.is_ice,
        }
        for o in order__all
    ])


@app.route('/data_analysis')
def order_data_analysis():
    db_session = DBSession()
    order__all = db_session.query(MineOrder).all()
    list_ = [(o.mine_name, o.price, o.volume, o.is_ice)
             for o in order__all]
    # todo 直接从db中读取df
    df = create_df(list_)
    df = process_df(df)
    return df.to_html()


@app.route('/order_delete')
def order_delete():
    db_session = DBSession()
    db_session.query(MineOrder).delete()
    db_session.commit()
    return 'delete success'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username_ = request.form['username']
        session['username'] = username_
        app.logger.debug('%s logged', username_)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    pop = session.pop('username')
    app.logger.info('%s logout', pop)
    return redirect(url_for('index'))


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name: str = None):
    return render_template('hello.html', name=name)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save(f'./tmp/{secure_filename(f.filename)}')
        return 'upload success'
    if request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
