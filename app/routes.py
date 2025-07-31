from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from .models import Epreuve
from .extensions import db


main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)


#PAGE D'ACCUEIL
@main_routes.route('/')
def home():
    return render_template('home.html')

@auth_routes.route('/connexion')
def login():
    pass