from flask import Flask,render_template
from . import main

@main.app_errorhandler(404)
def not_found(error):
    '''
    Function to render the 404 error page
    '''
    return render_template('404.html'),404