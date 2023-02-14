from app.api.main import main
from flask_json import json_response
from flask import request, session, redirect, url_for, flash
from flask.templating import render_template
from app.core.handlers import SalesHandler
from app.core.processes import SpecialProcess
from app.common.querysets import ProductListQuerySet
from functools import wraps
from datetime import datetime
from app.settings.pyodbc import Connection


def is_authenticated():
    return session.get('authenticated', False)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)

    return wrapper


# @main.route('/')
# @main.route('/index', methods=['GET'])
# def index():
#     return json_response(
#         message="retos y simulaciones API"
#     )

@main.route('/')
@main.route('/index', methods=['GET'])
@login_required
def index():
    with Connection() as conn:
        products = ProductListQuerySet(conn).get(id=session.get('id'))

    today = datetime.today()

    month = f'0{today.month}' if today.month < 10 else today.month
    year = f'{today.year}'

    return render_template('index.html', year=year, month=month,
                           products=products)


@main.route('/commissions', methods=['POST'])
def commissions():

    with Connection() as conn:
        sp = SpecialProcess(conn, request)
        response = sp.make()

    today = datetime.today()

    year = f'{today.year}'

    return render_template('results.html', response=response.json,
                           status=response.status_code, query='commissions', year=year)


@main.route('/sales', methods=['GET'])
def sales():
    response = SalesHandler.run(request)

    today = datetime.today()

    year = f'{today.year}'

    return render_template('results.html', response=response.json,
                           status=response.status_code, query='sales', year=year)


@main.route('/about')
def about():
    today = datetime.today()

    year = f'{today.year}'

    return render_template('about.html', year=year)


# @main.route('/health')
# def about():
#     return json_response(
#         message="OK"
#     )


@main.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        flash('Ya estas autenticado.')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        _id = request.form.get('id')
        password = request.form.get('password')
        # TODO 1: Request to gana login API
        # response = requests.post(url=GANA_LOGIN_API, headers= headers)
        # TODO 2: Get credentials from request response to API
        # if response.ok:
        # session['id'] = response.json.id
        # session['token'] = response.json.token
        # else
        # show validation errors on login form
        # return redirect(url_for('login'))

        if _id == password:
            session['id'] = _id
            # cache.set('id', _id)
            session['token'] = password
            session['authenticated'] = True
            return redirect(url_for('main.index'))
        else:
            flash('Usuario o contraseña incorrecta')

    today = datetime.today()

    year = f'{today.year}'

    return render_template('login.html', year=year)


@main.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main.about'))
