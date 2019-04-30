from flask import render_template
from . import main

@main.app_errorhandler(404) #application-wide error handler  ie app_errorhandler
def four_Ow_four(error):
    '''
    Function to render the 404 error page
    '''
    return render_template('error.html'),404
#    Since we are defining our error handler inside our blueprint we import the blueprint instance main and use it to define our decorator.