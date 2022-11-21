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
                            f"<p>Please activate your your account by clicking on the following link:</strong> <br/> "
                            f"<a href='{link}'>CLICK TO "
                            f"CONFIRM "
                            f"EMAIL</a> </p>"
                            f"<p>If you have any queries please send it to <a "
                            f"href='mailto:lecturersevaluations@gimpa.edu.gh'>lecturersevaluations@gimpa.edu.gh</a"
                            f"></p> "
                            f"<br>"
                            f"Thank you<br>"
                            f"Your sincerely<br>"
                            f"APQAD GIMPA"
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