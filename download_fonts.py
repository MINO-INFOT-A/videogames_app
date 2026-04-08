import urllib.request
import re
import os

css_url = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
req = urllib.request.Request(css_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    css_content = urllib.request.urlopen(req).read().decode('utf-8')
    # Filter only latin subset to save space and time
    # Google fonts css structure: /* latin */\n@font-face { ... }
    # We will just parse all urls and download them. To make sure we don't download cyrillic/vietnamese we can just download them all, there usually aren't that many for one family.
    urls = set(re.findall(r'url\((https://[^)]+)\)', css_content))
    
    os.makedirs('app/static/fonts', exist_ok=True)
    
    for url in urls:
        filename = url.split('/')[-1]
        urllib.request.urlretrieve(url, f"app/static/fonts/{filename}")
        css_content = css_content.replace(url, f"../fonts/{filename}")
        
    with open('app/static/css/fonts.css', 'w') as f:
        f.write(css_content)
    print("Fonts downloaded successfully.")
except Exception as e:
    print(f"Error downloading fonts: {e}")
