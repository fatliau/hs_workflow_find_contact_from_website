import re
import requests
from urllib.parse import urlparse, urlunparse
from html.parser import HTMLParser
from urllib.parse import urljoin

class LinkParser(HTMLParser):
    def __init__(self, base_url, keywords):
        super().__init__()
        self.links = set()
        self.base_url = base_url
        self.keywords = keywords

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = None
            for attr, value in attrs:
                if attr == 'href':
                    href = value
                    break
            if href:
                # Convert relative URLs to absolute URLs if needed
                full_url = urljoin(self.base_url, href) if href.startswith('/') else href
                if any(keyword in href.lower() for keyword in self.keywords):
                    self.links.add(full_url)

    def get_links(self):
        return self.links


def find_contact_emails_aws_lambda(website_url):
    def ensure_valid_url(url):
        parsed_url = urlparse(url)
        # Check if the scheme is missing and add 'https' as default if necessary
        if not parsed_url.scheme:
            # Use only the netloc (hostname) if available, or fallback to the original path if no netloc is present
            if parsed_url.netloc:
                url = urlunparse(('https', parsed_url.netloc, parsed_url.path, '', '', ''))
            else:
                url = urlunparse(('https', parsed_url.path, '', '', '', ''))
        return url

    def fetch_contact_links(url):
        keywords = ["contact", "about", "us", "support", "contactus"]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            parser = LinkParser(url, keywords)
            parser.feed(response.text)
            return parser.get_links()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return set()

    def fetch_page_text(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    def extract_emails_from_text(text):
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?:com|org))'
        return re.findall(email_pattern, text)

    def email_filter(emails):
        ignored_domains = {'@example.com', 'wixpress.com', '@domain.com', '@godaddy.com', '@mystore.com',
                           'mysite.com', '@email.com', 'clyffordstillmuseum.org'}
        return set(filter(lambda s: not any(domain in s for domain in ignored_domains), emails))


    website_url = ensure_valid_url(website_url)
    links = set()
    links.add(website_url)
    links.update(fetch_contact_links(website_url))

    emails = set()

    for i, link in enumerate(links):
        text = fetch_page_text(link)
        if not text:
            if i == 0:
                print(f"Skipping all of {website_url} due to main page fetch error")
                return emails
            else:
                print(f"Skipping {link} due to fetch error.")
                continue
        emails.update(extract_emails_from_text(text))

    emails = email_filter(emails)
    emails = list(emails)
    if len(emails) > 0:
        return emails[0]
    else:
        return None

def main(event):
    # Fetch the website URL from inputFields
    website_url = event.get('inputFields', {}).get('website_url')
    if not website_url:
        return {
            "statusCode": 400,
            "body": "website_url parameter is missing in the inputFields."
        }

    # Extract email
    email = find_contact_emails_aws_lambda(website_url)
    if not email:
        return {
            "statusCode": 404,
            "body": "No email found for the given website."
        }

    # Return outputs to HubSpot workflow
    return {
        "outputFields": {
            "email": email if email else "No email found",
        }
    }
