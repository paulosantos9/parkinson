from django.shortcuts import render
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/main')
def main():
    return '<h1>Created with success</h1>'