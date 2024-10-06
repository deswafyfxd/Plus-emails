import os
import requests
import yaml

def send_to_discord(emails, webhook_url):
    for email in emails:
        response = requests.post(webhook_url, json={"content": email})
        if response.status_code == 200:
            print(f"Successfully sent {email} to Discord")
        else:
            print(f"Failed to send {email} to Discord, status code: {response.status_code}")

def main():
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("No Discord webhook URL provided.")
        return

    with open('control.yaml', 'r') as f:
        control = yaml.safe_load(f)
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    with open('character_constraints.yaml', 'r') as f:
        constraints = yaml.safe_load(f)

    gmail_enabled = control['gmail']
    outlook_enabled = control['outlook']
    custom_domains_enabled = control['custom_domains']
    email_validation_enabled = control['email_validation']
    use_personal_names = config['use_personal_names']
    add_numbers = config['adding_numbers']
    numbers_count = config['numbers_count']
    max_email_length = config['max_email_length']
    name_category = None
    
    if use_personal_names['indian']:
        name_category = "indian"
    elif use_personal_names['western']:
        name_category = "western"
    elif use_personal_names['japanese']:
        name_category = "japanese"
    elif use_personal_names['chinese']:
        name_category = "chinese"
    elif use_personal_names['other']:
        name_category = "other"

    use_first_name = use_personal_names['first_name']
    use_last_name = use_personal_names['last_name']
    
    domains = []
    if gmail_enabled:
        domains.append("gmail.com")
    if outlook_enabled:
        domains.append("outlook.com")
    if custom_domains_enabled:
        domains.extend(config['custom_domains_list'])
    
    popular_domains = control.get('use_popular_domains', {})
    if popular_domains.get('yahoo', False):
        domains.append("yahoo.com")
    if popular_domains.get('hotmail', False):
        domains.append("hotmail.com")
    if popular_domains.get('aol', False):
        domains.append("aol.com")
    if popular_domains.get('icloud', False):
        domains.append("icloud.com")
    if popular_domains.get('proton', False):
        domains.append("proton.me")
    if popular_domains.get('gmx', False):
        domains.append("gmx.com")
    
    for domain in domains:
        base = config.get(f"{domain.split('.')[0]}_base")
        if base:
            count = config.get(f"{domain.split('.')[0]}_count", 0)
            if count == 0:
                print(f"No email count specified for {domain}, skipping.")
                continue
            emails = generate_emails(base, domain, count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_email_length, constraints)
            send_to_discord(emails, webhook_url)

if __name__ == "__main__":
    main()
