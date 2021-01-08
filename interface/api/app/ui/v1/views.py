from http import HTTPStatus
import socket

from flask import render_template

from . import forms, ui


@ui.route('/accepted', methods=['GET'])
def accepted():
    return render_template(
        'accepted.html',
        form=forms.Accepted(),
        hostname=socket.gethostname()
    ), HTTPStatus.ACCEPTED


@ui.route('/healthz', methods=['GET'])
def healthz():
    return render_template(
        'ok.html',
        form=forms.Ok()
    ), HTTPStatus.OK


@ui.route('/', methods=['GET'])
def index():
    return render_template(
        'not_found.html',
        form=forms.NotFound(),
    ), HTTPStatus.NOT_FOUND
