import os
import requests

def send_to_discord(file_path, webhook_url):
    with open(file_path, 'rb') as f:
        response = requests.post(
            webhook_url,
            files={"file": f}
        )
        if response.status_code == 200:
            print(f"Successfully sent {file_path} to Discord")
        else:
            print(f"Failed to send {file_path} to Discord, status code: {response.status_code}")

def main():
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("No Discord webhook URL provided.")
        return

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith("_emails.txt"):
                file_path = os.path.join(root, file)
                send_to_discord(file_path, webhook_url)

if __name__ == "__main__":
    main()
