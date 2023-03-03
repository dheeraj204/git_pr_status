import smtplib
from git_data import RepositoryData
from email.message import EmailMessage


def attach_logs_remainder(receiver_mail_id, pr_number, repo):
    # E-mail sender ID
    email_sender = RepositoryData.data['sender_mail_id']

    # Sender E-mail password
    email_password = RepositoryData.data['sender_password']

    # E-mail Receiver ID
    email_receiver = receiver_mail_id

    # Subject for the E-mail
    subject = f'Remainder to attach logs in PR#{pr_number}'

    # Body of the message to be sent
    body = f"Failed to attach logs please attach the logs in PR#{pr_number}in {repo} "

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(email_sender, email_password)

    # sending the mail
    s.sendmail(email_sender, email_receiver, em.as_string())

    # terminating the session
    s.quit()


def check_logs(extensions, comments):
    for ext in extensions:
        res = [comment for comment in comments if ext in comment]
        if len(res) > 0:
            return True
