import os

from qapd.settings import mailjet


def send_mail(to_email, to_name, subject, message):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.getenv('EMAIL_HOST_USER'),
                    "Name": os.getenv('EMAIL_HOST_USERNAME')
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_name
                    }
                ],
                "Subject": subject,
                "TextPart": message,
                "HTMLPart": message
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())


def send_bulk_mail(bulk_contacts, subject, message):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.getenv('EMAIL_HOST_USER'),
                    "Name": os.getenv('EMAIL_HOST_USERNAME')
                },
                "To": bulk_contacts,
                "Subject": subject,
                "TextPart": message,
                "HTMLPart": message
            }
        ]
    }

    result = mailjet.send.create(data=data)

def generate_confirmation_link_mail(to_email, to_name, link):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.getenv('EMAIL_HOST_USER'),
                    "Name": os.getenv('EMAIL_HOST_USERNAME')
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_name
                    }
                ],
                "Subject": "Activate your GIMPA APQAD account!",
                "TextPart": f"Activate your account by clicking on the following link: {link}",
                "HTMLPart": f"<div style='font-size:18px; line-height:1.6;color: rgb(48,55,61);"
                            f"font-family: proxima-nova,'Helvetica Neue',Helvetica,Helvetica,Arial,sans-serif;'>"
                            f"<h4>Dear {to_name.capitalize()},</h4>"
                            f"<p>Thank you for registering with Academic Planning and Quality Assurance Department "
                            f"Portal. </p>"
                            f"<p>We have moved our lecturer evaluation online!</p>"
                            f"<p>To activate your account, please click on the following link:<br/> "
                            f"<a href='{link}'>CLICK HERE"
                            f"</a> </p>"
                            f"If you can't see the link, please copy and paste this link:{link} into your browser to"
                            f" activate your account"
                            f"<p>If you have any queries please send it to <a "
                            f"href='mailto:lecturersevaluations@gimpa.edu.gh'>lecturersevaluations@gimpa.edu.gh</a"
                            f"></p> "
                            f"<br>"
                            f"Thank you<br>"
                            f"Your sincerely<br>"
                            f"Director <br/>"
                            f"APQAD GIMPA <br/>"
                            f"<a href='https://www.gimpa.edu.gh'>GIMPA</a>"
                            f"</div>"


            }
        ]
    }

    result = mailjet.send.create(data=data)
    if result:
        print(result.status_code,"email sent", result.json())
        return True
    else:
        print(result.status_code,"email not sent", result.json())

        return False