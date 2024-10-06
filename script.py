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
    for _ in range(count):
        first_name = faker.first_name().lower()
        last_name = faker.last_name().lower()
        name = f"{first_name}{last_name}"
        
        email = f"{base}+{sanitize_email(name)}@{domain}"
        
        if is_valid_email(email):
            emails.append(email)
    
    print(f"Generated emails for {base} @ {domain}: {emails}")
    return emails

def main():
    with open('control.yaml', 'r') as f:
        control = yaml.safe_load(f)
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    gmail_enabled = control['gmail']
    outlook_enabled = control['outlook']
    
    domains = []
    if gmail_enabled:
        domains.append("gmail.com")
    if outlook_enabled:
        domains.append("outlook.com")
    
    for domain in domains:
        base = config.get(f"{domain.split('.')[0]}_base")
        if base:
            count = config.get(f"{domain.split('.')[0]}_count", 5)  # Use a small number for testing
            emails = generate_emails(base, domain, count)

if __name__ == "__main__":
    main()
