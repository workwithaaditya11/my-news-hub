import feedparser
import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone
import hashlib

# ============================================================
# CONFIG — GitHub Secrets बाट आउँछ (तपाईंले set गर्नुपर्छ)
# ============================================================
SENDER_EMAIL    = os.environ['workwithaaditya11@gmail.com']     # तपाईंको Gmail
SENDER_PASSWORD = os.environ['dougtoljijyqiakz']  # Gmail App Password
RECEIVER_EMAIL  = os.environ['thesiscraftnepaledu@gmail.com']   # जहाँ news पठाउने

# ============================================================
# RSS FEEDS
# ============================================================
FEEDS = [
    {'url': 'https://feeds.bbci.co.uk/news/world/rss.xml',        'source': 'BBC News',     'cat': 'Geopolitics'},
    {'url': 'https://feeds.reuters.com/reuters/topNews',           'source': 'Reuters',      'cat': 'Geopolitics'},
    {'url': 'https://www.aljazeera.com/xml/rss/all.xml',          'source': 'Al Jazeera',   'cat': 'Conflict'},
    {'url': 'https://rss.theguardian.com/theguardian/world/rss',  'source': 'The Guardian', 'cat': 'Politics'},
    {'url': 'https://feeds.feedburner.com/ndtvnews-world-news',    'source': 'NDTV World',   'cat': 'Geopolitics'},
    {'url': 'https://www.onlinekhabar.com/feed',                   'source': 'OnlineKhabar', 'cat': '🇳🇵 Nepal'},
    {'url': 'https://www.setopati.com/feed',                       'source': 'Setopati',     'cat': '🇳🇵 Nepal'},
    {'url': 'https://ratopati.com/feed',                           'source': 'Ratopati',     'cat': '🇳🇵 Nepal'},
]

SEEN_FILE = 'seen_news.json'

# ============================================================
# HELPERS
# ============================================================
def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    # Keep only last 500 to avoid file bloat
    seen_list = list(seen)[-500:]
    with open(SEEN_FILE, 'w') as f:
        json.dump(seen_list, f)

def news_id(entry):
    return hashlib.md5((entry.get('link','') + entry.get('title','')).encode()).hexdigest()

def fetch_new_articles(seen):
    new_articles = []
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info['url'])
            for entry in feed.entries[:15]:
                nid = news_id(entry)
                if nid not in seen:
                    new_articles.append({
                        'id':      nid,
                        'title':   entry.get('title', 'No title'),
                        'summary': entry.get('summary', '')[:200].strip(),
                        'link':    entry.get('link', '#'),
                        'source':  feed_info['source'],
                        'cat':     feed_info['cat'],
                    })
        except Exception as e:
            print(f"Error fetching {feed_info['source']}: {e}")
    return new_articles

# ============================================================
# EMAIL HTML TEMPLATE
# ============================================================
CAT_COLORS = {
    'Geopolitics': '#457b9d',
    'Politics':    '#c77dff',
    'Conflict':    '#e63946',
    '🇳🇵 Nepal':  '#ff6b35',
    'Economy':     '#2dc653',
}

def build_email(articles):
    now = datetime.now(timezone.utc).strftime('%B %d, %Y · %H:%M UTC')

    cards_html = ''
    for a in articles[:20]:   # max 20 per email
        color = CAT_COLORS.get(a['cat'], '#888')
        summary = f"<p style='margin:6px 0 0;font-size:13px;color:#aaa;line-height:1.5'>{a['summary']}...</p>" if a['summary'] else ''
        cards_html += f"""
        <a href="{a['link']}" target="_blank" style="display:block;text-decoration:none;color:inherit;
           background:#1e1e24;border:1px solid #2a2a35;border-left:3px solid {color};
           border-radius:8px;padding:14px 16px;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
            <span style="background:{color}20;color:{color};font-size:10px;font-weight:700;
              padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:0.5px">{a['cat']}</span>
            <span style="font-size:11px;color:#666">{a['source']}</span>
          </div>
          <p style="margin:0;font-size:15px;font-weight:600;color:#e8e8f0;line-height:1.4">{a['title']}</p>
          {summary}
        </a>"""

    html = f"""
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0d0d0f;font-family:'Segoe UI',system-ui,sans-serif">
  <div style="max-width:640px;margin:0 auto;padding:24px">

    <!-- Header -->
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <div style="width:10px;height:10px;border-radius:50%;background:#e63946"></div>
      <h1 style="margin:0;font-size:20px;color:#e8e8f0">Global<span style="color:#e63946">News</span> Update</h1>
      <span style="background:#e63946;color:#fff;font-size:10px;font-weight:700;
        padding:2px 7px;border-radius:3px;letter-spacing:0.5px">LIVE</span>
    </div>
    <p style="margin:0 0 20px;font-size:12px;color:#555">{now} · {len(articles)} new articles</p>

    <!-- Cards -->
    {cards_html}

    <!-- Footer -->
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid #2a2a35;
      font-size:12px;color:#444;text-align:center">
      GlobalNews · Auto-sent when new articles detected · <a href="#" style="color:#457b9d">Unsubscribe</a>
    </div>
  </div>
</body>
</html>"""
    return html

# ============================================================
# SEND EMAIL
# ============================================================
def send_email(articles):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🌐 {len(articles)} New Articles — GlobalNews Update"
    msg['From']    = SENDER_EMAIL
    msg['To']      = RECEIVER_EMAIL

    html = build_email(articles)
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

    print(f"✅ Email sent: {len(articles)} new articles")

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    seen = load_seen()
    new_articles = fetch_new_articles(seen)

    if new_articles:
        send_email(new_articles)
        seen.update(a['id'] for a in new_articles)
        save_seen(seen)
        print(f"Found {len(new_articles)} new articles")
    else:
        print("No new articles found")
