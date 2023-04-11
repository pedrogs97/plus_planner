"""Project email sender"""
from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


class SendinblueEmailSender:
    """Class of email sender"""

    def __init__(self) -> None:
        """Init Email sender."""
        if settings.SMTP_KEY is None or settings.SMTP_KEY == "":
            raise ValueError("API KEY empty.")
        self.__configuration = sib_api_v3_sdk.Configuration()
        self.__configuration.api_key["api-key"] = settings.SMTP_KEY

        self.__api_instance_transactional = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(self.__configuration)
        )
        self.__send_smtp_email = None

    def build_email(
        self,
        email_content: dict,
        sender: dict,
        reply_to: dict,
        reciver: list[dict],
    ):
        """
        Build Sendinblue email.

        Params:
            email_content: { html_content: str (always html code), subject: str }
            sender: { name: str, email: str }
            reply_to: { name: str, email: str }
            reciver: [ { email: str, name: str } ]
        """
        self.__send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=reciver,
            reply_to=reply_to,
            html_content=email_content["html_content"],
            sender=sender,
            subject=email_content["subject"],
        )

    def send_email(self):
        """Send email via Sendinblue."""
        try:
            if self.__send_smtp_email is None:
                raise ValueError("Email not built.")
            self.__api_instance_transactional.send_transac_email(self.__send_smtp_email)
        except ApiException:
            print("Unable to send email")
