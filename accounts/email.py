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
                # "HTMLPart": message
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