from mailjet_rest import Client
import os



def get_mailjet_settings():
    with open('data/mailjet_settings.txt', mode='r') as txt_file:
        lines = []
        for line in txt_file:
            lines.append(line.strip('\n'))
    lines[0] 
    if not lines:
        raise ValueError('File is empty')
    return lines


credentials = get_mailjet_settings() 
api_key = credentials[0]
api_secret_key = credentials[1]
mailjet = Client(auth=(api_key, api_secret_key), version='v3.1')


def create_email_for_creation_of_ad(recipient_email: str, recipient_name: str):
    json = {
  'Messages': [
    {
      "From": {
        "Email": "jobmatch@abv.bg", 
        "Name": "JobMatch Team"
      },
      "To": [
        {
          "Email": recipient_email,
          "Name": recipient_name
        }
      ],
      "Subject": "Congratulations, your ad is now live!",
      "TextPart": "Congratulations, your ad is now live!",
      "HTMLPart": "<h3>Congratulations, your ad is now live! Your future coworkers await you!",
      "CustomID": "LiveAd"
    }
  ]
}

    return json


def create_email_for_update_of_ad(recipient_email: str, recipient_name: str):
    json = {
  'Messages': [
    {
      "From": {
        "Email": "jobmatch@abv.bg",
        "Name": "JobMatch Team"
      },
      "To": [
        {
          "Email": recipient_email, 
          "Name": recipient_name
        }
      ],
      "Subject": "Ad successfully updated!",
      "TextPart": "Ad successfully updated!",
      "HTMLPart": "<h3>Ad successfully updated!",
      "CustomID": "LiveAd"
    }
  ]
}

    return json


def create_email_for_update_of_ad(recipient_email: str, recipient_name: str):
    json = {
  'Messages': [
    {
      "From": {
        "Email": "jobmatch@abv.bg",
        "Name": "JobMatch Team"
      },
      "To": [
        {
          "Email": recipient_email, 
          "Name": recipient_name
        }
      ],
      "Subject": "Ad successfully updated!",
      "TextPart": "Ad successfully updated!",
      "HTMLPart": "<h3>Ad successfully updated!",
      "CustomID": "UpdatedAd"
    }
  ]
}

    return json


def create_email_for_deleting_ad(recipient_email: str, recipient_name: str):
    json = {
  'Messages': [
    {
      "From": {
        "Email": "jobmatch@abv.bg",
        "Name": "JobMatch Team"
      },
      "To": [
        {
          "Email": recipient_email, 
          "Name": recipient_name
        }
      ],
      "Subject": "Ad successfully deleted.",
      "TextPart": "Ad successfully deleted.",
      "HTMLPart": "<h3>Ad successfully deleted.",
      "CustomID": "DeletedAd"
    }
  ]
}

    return json


def create_email_for_update_of_ad(recipient_email: str, recipient_name: str):
    json = {
  'Messages': [
    {
      "From": {
        "Email": "jobmatch@abv.bg",
        "Name": "JobMatch Team"
      },
      "To": [
        {
          "Email": recipient_email, 
          "Name": recipient_name
        }
      ],
      "Subject": "Ad successfully updated!",
      "TextPart": "Ad successfully updated!",
      "HTMLPart": "<h3>Ad successfully updated!",
      "CustomID": "UpdatedAd"
    }
  ]
}

    return json

def create_email_for_a_match_request(recipient_email: str, recipient_name: str):
    json = {
  'Messages': [
    {
      "From": {
        "Email": "jobmatch@abv.bg",
        "Name": "JobMatch Team"
      },
      "To": [
        {
          "Email": recipient_email, 
          "Name": recipient_name
        }
      ],
      "Subject": "Congratulations! You have a match request!",
      "TextPart": "Congratulations! You have a match request!",
      "HTMLPart": "<h3>Congratulations! You have a match request!",
      "CustomID": "NewMatch"
    }
  ]
}

    return json

def create_email_for_a_match_confirmation(recipient_email: str, recipient_name: str):
    json = {
  'Messages': [
    {
      "From": {
        "Email": "jobmatch@abv.bg",
        "Name": "JobMatch Team"
      },
      "To": [
        {
          "Email": recipient_email, 
          "Name": recipient_name
        }
      ],
      "Subject": "Congratulations! Your match request has been confirmed!",
      "TextPart": "Congratulations! Your match request has been confirmed!",
      "HTMLPart": "<h3>Congratulations! Your match request has been confirmed!",
      "CustomID": "MatchConfirm"
    }
  ]
}

    return json








