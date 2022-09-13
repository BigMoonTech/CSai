from flask import Blueprint, redirect
from src.infrastructure.view_modifier import response
import src.infrastructure.cookie_auth as cookie_auth
from src.services import user_service
from src.view_models.account.register_viewmodel import RegisterViewModel
from src.view_models.account.login_viewmodel import LoginViewModel
from src.view_models.account.index_viewmodel import IndexViewModel


blueprint = Blueprint('account', __name__, template_folder='templates')

# ################### INDEX ####################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    # todo: complete the account index page
    viewmodel = IndexViewModel()
    return viewmodel.to_dict()


# ################### REGISTER #################################


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    viewmodel = RegisterViewModel()
    return viewmodel.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    viewmodel = RegisterViewModel()
    viewmodel.validate()

    if viewmodel.error:
        return viewmodel.to_dict()

    user = user_service.create_user(viewmodel.name, viewmodel.email, viewmodel.password)
    if not user:
        viewmodel.error = 'The account could not be created.'
        return viewmodel.to_dict()

    resp = redirect('/account/login')
    cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGIN ####################################


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    viewmodel = LoginViewModel()
    viewmodel.validate()

    if viewmodel.error:
        return viewmodel.to_dict()

    user = user_service.login_user(viewmodel.email, viewmodel.password)

    if user is None:
        viewmodel.error = 'Invalid email or password.'
        return viewmodel.to_dict()

    resp = redirect('/')
    cookie_auth.set_auth(resp, user.id)

    return resp


# ################### LOGOUT ###################################

@blueprint.route('/account/logout')
def logout():
    resp = redirect('/')
    cookie_auth.logout(resp)
    return resp