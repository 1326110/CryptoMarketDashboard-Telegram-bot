# Pre-Submission Review Checklist

Use this checklist before submitting MarketPulse for Telegram ad review or before sharing with a reviewer.

---

## Profile Setup

- [ ] High-resolution avatar uploaded (≥512x512 px)
- [ ] Bio set — no profit language, no banned terms
- [ ] Description set — accurately lists all features
- [ ] Commands registered via @BotFather
- [ ] Username is clean, branded (e.g., `@MarketPulseBot`)

---

## Bot Functionality

- [ ] `/start` responds instantly with the dashboard menu
- [ ] All inline buttons navigate correctly
- [ ] Price check works for multiple cryptocurrencies
- [ ] Top coins displays 10 entries
- [ ] Price alerts can be created and removed
- [ ] Portfolio holdings can be added and removed
- [ ] "Back to Dashboard" returns to main menu on every screen
- [ ] Empty states handled (no alerts, empty portfolio)
- [ ] Error states handled (invalid coin name, API failure)

---

## Message Content

- [ ] No profit language anywhere ("earn", "profit", "return", "gain", "income")
- [ ] No banned phrases ("buy now", "best", "#1", "guaranteed", "risk-free")
- [ ] No ALL CAPS text (except cryptocurrency symbols like BTC)
- [ ] No imperative commands ("click here", "buy", "start now")
- [ ] No external links (all navigation is inline keyboard callbacks)
- [ ] No line breaks in messages (short paragraphs only)
- [ ] Tone is neutral, factual, professional
- [ ] Max 1–3 emojis per message
- [ ] No spaced text, ASCII art, or excessive formatting

---

## Compliance Documents

- [ ] `COMPLIANCE.md` reviewed — all ✅ items confirmed
- [ ] `AD_COPY.md` selected ad variant meets 160-char limit
- [ ] `BOT_PROFILE.md` profile settings applied
- [ ] `/privacy` command returns privacy policy
- [ ] `/terms` command returns terms of use

---

## Pre-Launch Environment

- [ ] Bot has been running for ≥14 days (30 ideal)
- [ ] Hosted on a stable VPS or server (consistent IP)
- [ ] No VPN hopping or IP changes during review period
- [ ] No other bots sharing the same infrastructure pattern
- [ ] Realistic engagement (not suddenly spiking)

---

## Ad Submission

- [ ] Ad copy ≤ 160 characters
- [ ] Only 1 Telegram-native link (`@username`)
- [ ] No line breaks in ad text
- [ ] No imperative commands or persuasion language
- [ ] Ad promise matches actual bot features
- [ ] Ad is unique — not reused from another campaign

---

## Final Checks

```diff
+ /start responds instantly
+ All features accessible without login/payment
+ No banned content (adult, gambling, illegal)
+ No financial advice claims
+ Data handling disclosed in /privacy
+ Terms of use disclosed in /terms
+ Profile is complete and professional
+ Ad copy is compliant
```
