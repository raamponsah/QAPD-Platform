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
                "HTMLPart": f"<div>"
                            f"Dear {to_name},<br>"
                            f"Please activate your your account by clicking on the following link:</strong> <br/> "
                            f"<a href='{link}' style='background:rgb(0, 110, 255); "
                            f"border-radius:10px;text-align:center;width:400px;color:white;text-decoration:none"
                            f";padding:1rem; "
                            f"margin:1rem auto;display:flex;justify-content:center; align-items:center'>CLICK TO "
                            f"CONFIRM "
                            f"EMAIL</a> "
                            f"<br>"
                            f"Thank you<br>"
                            f"Your sincerely<br>"
                            f"APQAD GIMPA"
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