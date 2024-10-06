import yaml
import os

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    bases = [
        config['gmail_base'],
        config['outlook_base'],
        config['popular_domains']['yahoo_base'],
        config['popular_domains']['hotmail_base'],
        config['popular_domains']['aol_base'],
        config['popular_domains']['icloud_base'],
        config['popular_domains']['proton_base'],
        config['popular_domains']['gmx_base']
    ]

    for base in bases:
        domain = base.split('@')[1].split('.')[0]
        if not os.path.exists(domain):
            os.makedirs(domain)
        file_name = f'{base.replace("@", "_")}_emails.txt'
        if os.path.exists(f'{domain}/{file_name}'):
            counter = 1
            while os.path.exists(f'{domain}/{base.replace("@", "_")}_emails_{counter}.txt'):
                counter += 1
            file_name = f'{base.replace("@", "_")}_emails_{counter}.txt'
        if os.path.exists(file_name):
            os.rename(file_name, f'{domain}/{file_name}')

if __name__ == "__main__":
    main()
