"""Client para comunicacao com sendgrid"""

import json
import tempfile
import sendgrid
import requests
from sendgrid.helpers.mail import Email, Content, Mail

REQUIRE_CONFIG_KEYS = ["SENDGRID_API_KEY"]

class SendgridService:
    """
    Serviço para envio de emails via plataforma sendgrid.
    """

    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if any(k not in app.config for k in REQUIRE_CONFIG_KEYS):
            raise ValueError('{0} is required'.format(REQUIRE_CONFIG_KEYS))
        token = app.config["SENDGRID_API_KEY"]
        self.sg = sendgrid.SendGridAPIClient(apikey=token)

    def send_msg(self, from_mail, to_mail, subject, content, content_type="text/plain"):
        from_mail = Email(from_mail)
        to_mail = Email(to_mail)
        content = Content(content_type, content)
        mail = Mail(from_mail, subject, to_mail, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)