import random
from faker import Faker
import yaml
import re

faker = Faker()

def sanitize_email(name):
    return name.replace(" ", "").replace(".", "").lower()

def is_valid_email(email):
    # Simple regex for email validation
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def apply_constraints(name, constraints):
    if constraints['use_all_constraints']:
        # Apply all constraints
        if constraints['allowed_characters']['use_allowed_characters']:
            if constraints['allowed_characters']['use_only_specific']:
                allowed_chars = set(constraints['allowed_characters']['specific_characters'])
                if constraints['allowed_characters']['combine_with_common']:
                    allowed_chars.update(constraints['allowed_characters']['combined_characters'])
            else:
                allowed_chars = set(constraints['allowed_characters']['common_characters'])
            name = ''.join(filter(lambda c: c in allowed_chars, name))
        
        if constraints['disallowed_characters']['use_disallowed_characters']:
            disallowed_chars = set(constraints['disallowed_characters']['characters'])
            name = ''.join(filter(lambda c: c not in disallowed_chars, name))
        
        if constraints['max_local_part_length']['use_max_local_part_length']:
            max_length = constraints['max_local_part_length']['length']
            name = name[:max_length]
        
        if constraints['min_local_part_length']['use_min_local_part_length']:
            min_length = constraints['min_local_part_length']['length']
            if len(name) < min_length:
                name = name.ljust(min_length, '0')
    
    return name

def generate_emails(base, domain, count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_length, constraints):
    emails = []
    for _ in range(count):
        first_name = ""
        last_name = ""
        if name_category == "western":
            first_name = faker.first_name().lower() if use_first_name else ""
            last_name = faker.last_name().lower() if use_last_name else ""
        elif name_category == "indian":
            faker.add_provider(faker.providers.person.en_IN)
            first_name = faker.first_name().lower() if use_first_name else ""
            last_name = faker.last_name().lower() if use_last_name else ""
        elif name_category == "japanese":
            faker.add_provider(faker.providers.person.ja_JP)
            first_name = faker.first_name().lower() if use_first_name else ""
            last_name = faker.last_name().lower() if use_last_name else ""
        elif name_category == "chinese":
            faker.add_provider(faker.providers.person.zh_CN)
            first_name = faker.first_name().lower() if use_first_name else ""
            last_name = faker.last_name().lower() if use_last_name else ""
        else:
            first_name = faker.first_name().lower() if use_first_name else ""
            last_name = faker.last_name().lower() if use_last_name else ""

        name = f"{first_name}{last_name}"
        name = apply_constraints(name, constraints)
        
        if add_numbers:
            numbers = ''.join([str(random.randint(0, 9)) for _ in range(numbers_count)])
            name = f"{name}{numbers}"

        email = f"{base}+{sanitize_email(name)}@{domain}"
        
        if len(email) > max_length:
            # Truncate the name part to fit within the max length
            max_name_length = max_length - len(f"{base}+@{domain}")
            email = f"{base}+{sanitize_email(name[:max_name_length])}@{domain}"
        
        if is_valid_email(email):
            emails.append(email)
    return emails

def write_to_file(filename, emails):
    with open(filename, 'w') as f:
        for email in emails:
            f.write(f"{email}\n")

def main():
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
        base = config['yahoo_base']
        count = config['yahoo_count']
        yahoo_emails = generate_emails(base, "yahoo.com", count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_email_length, constraints)
        write_to_file("yahoo_emails.txt", yahoo_emails)
    if popular_domains.get('hotmail', False):
        base = config['hotmail_base']
        count = config['hotmail_count']
        hotmail_emails = generate_emails(base, "hotmail.com", count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_email_length, constraints)
        write_to_file("hotmail_emails.txt", hotmail_emails)
    if popular_domains.get('aol', False):
        base = config['aol_base']
        count = config['aol_count']
        aol_emails = generate_emails(base, "aol.com", count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_email_length, constraints)
        write_to_file("aol_emails.txt", aol_emails)
    if popular_domains.get('icloud', False):
        base = config['icloud_base']
        count = config['icloud_count']
        icloud_emails = generate_emails(base, "icloud.com", count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_email_length, constraints)
        write_to_file("icloud_emails.txt", icloud_emails)
    if popular_domains.get('proton', False):
        base = config['proton_base']
        count = config['proton_count']
        proton_emails = generate_emails(base, "proton.me", count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_email_length, constraints)
        write_to_file("proton_emails.txt", proton_emails)
    if popular_domains.get('gmx', False):
        base = config['gmx_base']
        count = config['gmx_count']
        gmx_emails = generate_emails(base, "gmx.com", count, name_category, use_first_name, use_last_name, add_numbers, numbers_count, max_email_length, constraints)
        write_to_file("gmx_emails.txt", gmx_emails)

if __name__ == "__main__":
    main()
