"""Script to URL-encode spaces and em dashes in markdown links."""
import os
import re

def url_encode_links():
    """Identify and encode markdown links inside the foundation directory."""
    era_dir = "d:/code/ayan/contact/docs/0. Foundation and pre-product stabilization and codebase setup"
    pattern = re.compile(r'\[([^\]]+)\]\(((?:\./|\.\./)?0\.\d+(?:\.\d+)?(?:(?:%20|\s)(?:%E2%80%94|—)(?:%20|\s))?[^)]+\.md)\)')

    for filename in os.listdir(era_dir):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(era_dir, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        def repl(match):
            text = match.group(1)
            raw_link = match.group(2)
            # Encode spaces and em dashes safely
            decoded_link = raw_link.replace('%20', ' ').replace('%E2%80%94', '—')
            encoded_link = decoded_link.replace(' ', '%20').replace('—', '%E2%80%94')
            return f"[{text}]({encoded_link})"

        new_content, count = pattern.subn(repl, content)
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {count} links in {filename}")

if __name__ == "__main__":
    url_encode_links()
