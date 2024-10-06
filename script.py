import random
from faker import Faker
import yaml
import os
import re

faker = Faker()

def sanitize_email(name):
    return name.replace(" ", "").replace(".", "").lower()

def is_valid_email(email):
    # Simple regex for email validation
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def generate_emails(base, domain, count):
    emails = []
    print(f"Generating emails for base: {base}, domain: {domain}, count: {count}")
    for _ in range(count):
        first_name = faker.first_name().lower()
        last_name = faker.last_name().lower()
        name = f"{first_name}{last_name}"
        
        email = f"{base}+{sanitize_email(name)}@{domain}"
        
        if is_valid_email(email):
            emails.append(email)
    
    print(f"Generated emails: {emails}")
    return emails

def main():
    print("Reading control.yaml")
    with open('control.yaml', 'r') as f:
        control = yaml.safe_load(f)
    print("Control config:", control)
    
    print("Reading config.yaml")
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print("Config config:", config)

    gmail_enabled = control['gmail']
    outlook_enabled = control['outlook']
    
    domains = []
    if gmail_enabled:
        domains.append("gmail.com")
    if outlook_enabled:
        domains.append("outlook.com")
    
    for domain in domains:
        base = config.get(f"{domain.split('.')[0]}_base")
        print(f"Base for domain {domain}: {base}")
        if base:
            count = config.get(f"{domain.split('.')[0]}_count", 5)  # Use a small number for testing
            print(f"Email count for {base} @ {domain}: {count}")
            emails = generate_emails(base, domain, count)

if __name__ == "__main__":
    main()
