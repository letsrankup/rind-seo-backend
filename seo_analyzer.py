import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import re

def advanced_seo_audit(url):
    if not url.startswith('http'):
        url = 'https://' + url
        
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    
    print("\n" + "="*60)
    print(f"🚀 STARTING ENTERPRISE SEO AUDIT FOR: {url}")
    print(f"🕒 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
        end_time = time.time()
        
        load_time = round(end_time - start_time, 2)
        page_size_kb = round(len(response.content) / 1024, 2)
        
        if response.status_code != 200:
            print(f"❌ CRITICAL ERROR: Target server returned status code {response.status_code}")
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        score = 100
        critical_bugs = 0
        warnings = 0
        
        print("📁 [1/5] SPEED & PERFORMANCE AUDIT")
        print(f"  ⚡ Page Load Time: {load_time} seconds")
        if load_time > 2.5:
            print("    ⚠️ Warning: Load time is high! Optimize server response or compress assets.")
            warnings += 1
            score -= 10
        else:
            print("    ✔ Excellent speed performance.")
            
        print(f"  📦 Total Page Size: {page_size_kb} KB")
        if page_size_kb > 500:
            print("    ⚠️ Warning: Page size exceeds 500KB. Consider code minification.")
            warnings += 1
            score -= 5

        print("-" * 50)
        print("🔒 [2/5] SECURITY & PROTOCOL AUDIT")
        
        # SSL & HTTP/2 protocol check base
        if url.startswith('https'):
            print("  ✔ SSL Certificate: Active (HTTPS enforced)")
        else:
            print("  ❌ SSL Certificate: Missing or insecure HTTP protocol used!")
            critical_bugs += 1
            score -= 25
            
        # Security Headers check
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        if 'clickjacking' if 'x-frame-options' in headers_lower else False:
            print("  ✔ Anti-Clickjacking Header Present.")
        else:
            print("  ⚠️ Warning: X-Frame-Options missing. Vulnerable to Clickjacking.")
            warnings += 1
            
        print("-" * 50)
        print("🔍 [3/5] METADATA & CRAWLABILITY AUDIT")
        
        # Title Tag Deep Check
        title = soup.find('title')
        if title and title.string:
            t_text = title.string.strip()
            t_len = len(t_text)
            print(f"  ✔ Title Tag: '{t_text}' ({t_len} chars)")
            if t_len < 40 or t_len > 65:
                print(f"    ⚠️ Warning: Length is {t_len}. Ideal length is 40-65 characters.")
                warnings += 1
                score -= 10
        else:
            print("  ❌ Critical Bug: Title tag is completely MISSING!")
            critical_bugs += 1
            score -= 25
            
        # Meta Description Deep Check
        meta_desc = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
        if meta_desc and meta_desc.get('content'):
            d_text = meta_desc.get('content').strip()
            d_len = len(d_text)
            print(f"  ✔ Meta Description: '{d_text[:60]}...' ({d_len} chars)")
            if d_len < 140 or d_len > 165:
                print(f"    ⚠️ Warning: Length is {d_len}. Ideal length is 140-165 characters.")
                warnings += 1
                score -= 10
        else:
            print("  ❌ Critical Bug: Meta description tag is completely MISSING!")
            critical_bugs += 1
            score -= 20
            
        # Canonical URL Check
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical and canonical.get('href'):
            print(f"  ✔ Canonical Tag Found: {canonical.get('href')}")
        else:
            print("  ⚠️ Warning: Missing Canonical Tag. Risks duplicate content issues.")
            warnings += 1
            score -= 8

        # Indexing directives
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        if robots_meta and robots_meta.get('content'):
            print(f"  ℹ Indexing Rule (Meta Robots): {robots_meta.get('content')}")
            if 'noindex' in robots_meta.get('content').lower():
                print("    🚨 ALERT: This page instructs Google NOT to index it (noindex)!")

        print("-" * 50)
        print("📝 [4/5] CONTENT STRUCTURE & SEMANTICS")
        
        # Heading Hierarchy Check
        h1s = soup.find_all('h1')
        h2s = soup.find_all('h2')
        h3s = soup.find_all('h3')
        
        print(f"  📊 Headings Found -> H1: {len(h1s)} | H2: {len(h2s)} | H3: {len(h3s)}")
        if len(h1s) == 0:
            print("  ❌ Critical Bug: <h1> tag missing! Google requires an H1 for context.")
            critical_bugs += 1
            score -= 20
        elif len(h1s) > 1:
            print(f"  ⚠️ Warning: Multiple H1 tags ({len(h1s)}) detected. Only 1 is best practice.")
            warnings += 1
            score -= 10
        else:
            print(f"    ✔ H1 Text: '{h1s[0].get_text().strip()}'")

        print("-" * 50)
        print("🖼 [5/5] IMAGES & ASSETS AUDIT")
        
        images = soup.find_all('img')
        total_imgs = len(images)
        missing_alt = 0
        broken_images_count = 0
        
        for img in images:
            src = img.get('src')
            alt = img.get('alt')
            if not alt or alt.strip() == "":
                missing_alt += 1
                
        print(f"  📷 Total Images Discovered: {total_imgs}")
        if missing_alt > 0:
            print(f"  ⚠️ Warning: {missing_alt} images do not have an 'alt' description attribute.")
            score -= min(12, missing_alt * 2)
            warnings += 1
        else:
            print("  ✔ All images contain appropriate alternative text attributes.")

        # Common Files Verification
        print("\n🌐 [BONUS] EXTERNAL FILE STATUS VERIFICATION")
        for asset in ['robots.txt', 'sitemap.xml']:
            asset_url = f"https://{domain}/{asset}"
            try:
                res = requests.head(asset_url, headers=headers, timeout=5)
                if res.status_code == 200:
                    print(f"  ✔ Found asset deployment: {asset_url}")
                else:
                    print(f"  ⚠️ File Deployment Missing (Status {res.status_code}): {asset_url}")
            except:
                print(f"  ⚠️ Network Timeout checking asset: {asset}")

        final_score = max(0, score)
        print("\n" + "="*60)
        print("📊 FINAL EXECUTIVE AUDIT SUMMARY")
        print("="*60)
        print(f"🏆 OVERALL SEO AUDIT HEALTH SCORE: {final_score} / 100")
        print(f"🔴 Critical Structural Bugs Found: {critical_bugs}")
        print(f"🟡 Minor Optimization Warnings  : {warnings}")
        print("="*60)

    except Exception as e:
        print(f"\n❌ SCRIPT CONNECTION BREAK: Failed to process target. Details: {str(e)}")

if __name__ == "__main__":
    # Client ki website ka domain ya URL yahan likhein
    target_website = "wikipedia.org"
    advanced_seo_audit(target_website)

