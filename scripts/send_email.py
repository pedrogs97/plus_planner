"""Script to test email API"""
from __future__ import print_function
from pprint import pprint
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def run():
    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key[
        "api-key"
    ] = "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"
    # create an instance of the API class
    # api_instance = sib_api_v3_sdk.AccountApi(sib_api_v3_sdk.ApiClient(configuration))
    api_instance_transactional = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
    subject = "from the Python SDK!"
    sender = {"name": "Sendinblue", "email": "contact@sendinblue.com"}
    reply_to = {"name": "Sendinblue", "email": "contact@sendinblue.com"}
    html_content = (
        "<html><body><h1>This is my first transactional email </h1></body></html>"
    )
    to_reciver = [{"email": "pedrogustavosantana97@gmail.com", "name": "No replay"}]
    params = {"parameter": "My param value", "subject": "New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to_reciver,
        reply_to=reply_to,
        html_content=html_content,
        sender=sender,
        subject=subject,
        params=params,
    )

    try:
        # Get your account information, plan and credits details
        # api_response = api_instance.get_account()
        # pprint(api_response)
        api_response_transactional = api_instance_transactional.send_transac_email(
            send_smtp_email
        )
        print(api_response_transactional)
    except ApiException as e:
        print("Exception when calling AccountApi->get_account: %s\n" % e)
