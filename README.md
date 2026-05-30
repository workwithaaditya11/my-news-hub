# 🌐 GlobalNews — Setup Guide

## के छ यो project मा?
| File | काम |
|------|-----|
| `index.html` | News website (GitHub Pages मा host हुन्छ) |
| `send_news.py` | News fetch गरेर email पठाउने script |
| `.github/workflows/news-email.yml` | GitHub Actions — हरेक 30 min मा automatically run |

---

## Step 1 — Gmail App Password बनाउनुस्

> तपाईंको normal Gmail password काम गर्दैन — App Password चाहिन्छ

1. [myaccount.google.com](https://myaccount.google.com) मा जानुस्
2. **Security** → **2-Step Verification** enable गर्नुस् (भएको छैन भने)
3. **Security** → Search "App passwords" → **Mail** छान्नुस्
4. Generate गर्नुस् → **16-character password** copy गर्नुस्

---

## Step 2 — GitHub मा repo बनाउनुस्

1. [github.com/new](https://github.com/new) मा जानुस्
2. Repository name: `my-news-hub` (जे राख्नुस्)
3. **Public** राख्नुस् (GitHub Pages को लागि)
4. Create repository

---

## Step 3 — Files upload गर्नुस्

VS Code मा terminal खोल्नुस् र run गर्नुस्:

```bash
cd news-site
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/my-news-hub.git
git push -u origin main
```
> `YOUR_USERNAME` आफ्नो GitHub username राख्नुस्

---

## Step 4 — Secrets set गर्नुस्

GitHub repo मा जानुस् → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

तीनवटा secret add गर्नुस्:

| Name | Value |
|------|-------|
| `SENDER_EMAIL` | तपाईंको Gmail (xxx@gmail.com) |
| `SENDER_PASSWORD` | Step 1 को 16-char App Password |
| `RECEIVER_EMAIL` | जहाँ news चाहिन्छ त्यो email |

---

## Step 5 — GitHub Pages enable गर्नुस्

1. Repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** → **/ (root)**
4. Save

केही मिनेटमा तपाईंको website live हुन्छ:
`https://YOUR_USERNAME.github.io/my-news-hub`

---

## Step 6 — Test गर्नुस्

1. Repo → **Actions** tab
2. **News Email Sender** workflow
3. **Run workflow** button थिच्नुस्
4. Email आयो कि नहेर्नुस् ✅

---

## System कसरी काम गर्छ?

```
हरेक 30 मिनेट
      ↓
GitHub Actions wake up हुन्छ
      ↓
send_news.py run हुन्छ
      ↓
8 वटा RSS feeds check हुन्छ
      ↓
नयाँ news भेटियो? → Email पठाउँछ
नयाँ छैन?        → चुपचाप बन्द हुन्छ
```

---

## ❓ Problems?

- **Email आएन** → Gmail मा Spam folder check गर्नुस्
- **Actions fail** → Actions tab मा red X थिचेर error हेर्नुस्
- **Website खुलेन** → 5 मिनेट कुर्नुस्, Pages deploy हुन समय लाग्छ
