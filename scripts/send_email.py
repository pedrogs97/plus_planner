def run():
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(
        from_email="pgls.dev@gmail.com",
        to_emails="pedrogustavosantana97@gmail.com",
        subject="Sending with Twilio SendGrid is Fun",
        html_content="<strong>and easy to do anywhere, even with Python</strong>",
    )
    try:
        sg = SendGridAPIClient(
            "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"
        )
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
