import yagmail

def send_welcome_email(receiver_email):
    try:
        sender = "your_email"  # Replace with your Gmail
        app_password = "your_app_pass"  # Use app password (not your Gmail password)
        subject = "Welcome to Dynamic KPI Dashboard!"
        body = f"""
        Hello 👋,

        🎉Welcome to the Dynamic KPI Dashboard — your one-stop solution to monitor, forecast, and gain insights into stocks!

        Start exploring your dashboard and track your portfolio like a pro.

        Best regards,  
        The MetricView Team
        """

        yag = yagmail.SMTP(user=sender, password=app_password)
        yag.send(to=receiver_email, subject=subject, contents=body)
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False