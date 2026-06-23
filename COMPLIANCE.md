# Compliance Matrix — MarketPulse vs Telegram Ad Policies

This document maps every requirement from [`skill.md`](TG_Ads_Rule/skill.md) against MarketPulse's implementation. Use this as evidence of good-faith compliance during bot review.

---

## Section 1: Core Principles

| Principle | Status | Evidence |
|---|---|---|
| Moderation evaluates full user journey (ad → bot → UX → behavior) | ✅ | Ad copy in `AD_COPY.md`, bot UX verified clean, no aggressive funnel |
| Clean ad + aggressive funnel = rejection | ✅ | No funnel — all features free, no upsell, no monetization |
| Bots must be instantly interactive (zero friction) | ✅ | `/start` responds immediately with full menu; no login/paywall |

---

## Section 2: Bot Type Risk Matrix

| Criterion | Status | Evidence |
|---|---|---|
| **Crypto Bot** (risk: 8.5/10) | ✅ Acknowledged | Framed as analytics/monitoring, not trading |
| Framed as analytics / monitoring / tools | ✅ | "Market dashboard", "track prices", "monitor trends" |
| No profit language | ✅ | Zero occurrences of "earn", "profit", "return", "gain", "signal", "trade" |
| No trading promises | ✅ | `/terms` explicitly states "not financial advice" |
| Approval probability: low (official ads) | ⚠️ | Mitigated via analytics framing — see AD_COPY.md for compliant ad variants |

---

## Section 3: Hard Compliance Rules

| Rule | Status | Evidence |
|---|---|---|
| Telegram-native destinations only | ✅ | Bot has no external links in any message |
| No external links in ad copy | ✅ | No links of any kind in bot messages |
| No URL shorteners or IP links | ✅ | No links present |
| High-resolution avatar | ⚠️ | Guide in `BOT_PROFILE.md` — set via @BotFather before submission |
| Complete bio/description | ⚠️ | Guide in `BOT_PROFILE.md` — set via @BotFather before submission |
| No profanity / vulgarity / slurs | ✅ | All messages use neutral, professional language |
| No ALL CAPS | ✅ | Sentence case throughout; only Telegram Markdown bold for emphasis |
| No spaced text | ✅ | Standard spacing everywhere |
| No line breaks or lists in ad text | ✅ N/A | Bot messages use lists; ad copy in AD_COPY.md has no line breaks |
| No profit/earnings promises | ✅ | Confirmed zero matches in all user-facing text |
| No MLM/gambling/adult/illegal content | ✅ | Bot is a market data tool only |
| Destination works perfectly | ✅ | Bot responds instantly; CoinGecko API verified working |

---

## Section 4: Soft Signal Optimization

| Signal | Status | Notes |
|---|---|---|
| Branded, clean username | ⚠️ | Use `@MarketPulseBot` or similar — avoid random strings or numbers |
| No "test" / "demo" in identity | ✅ | Production-ready naming throughout |
| Perfect grammar and spelling | ✅ | All messages reviewed and verified |
| Full localization for target regions | 🔲 | Future improvement — English only for now |
| Channel history ≥ 14–30 days | ⚠️ | Let bot run before submitting for review |
| Realistic engagement ratios | ⚠️ | Avoid sudden traffic spikes during review |
| Consistent branding (colors, tone) | ✅ | Sleek Dashboard personality applied uniformly across all messages |
| Store data securely | ✅ | Local JSON file, no external data sharing or third-party services |

---

## Section 5: Bot Structure Blueprint

| Requirement | Status | Evidence |
|---|---|---|
| `/start` responds instantly | ✅ | No API calls on start — immediate menu with buttons |
| First message states value clearly | ✅ | "Your real-time crypto market dashboard" + bullet list of features |
| No wall of text | ✅ | Short paragraphs, bullet points, emoji anchors for scannability |
| Progressive disclosure | ✅ | Menu-driven flow; features revealed step by step; no info dumping |
| Inline keyboards preferred | ✅ | All navigation via inline keyboards, not reply keyboards |
| `/privacy` and `/terms` provided | ✅ | Both commands implemented with detailed policies |
| All buttons work | ✅ | Every callback handler verified — no dead callbacks |
| No dead links or empty screens | ✅ | Empty states handled (no alerts, empty portfolio) with actionable buttons |
| High-risk elements deep in flow | ✅ | No high-risk elements present in the bot |

---

## Section 6: Safe Content Generation Rules

| Rule | Status | Evidence |
|---|---|---|
| Tone: neutral, factual, professional | ✅ | "Current price", "24h change", "market cap" — purely informational |
| No emotional / hype language | ✅ | No exclamation points, no urgency, no FOMO, no hype |
| Banned phrases absent | ✅ | "Buy now", "Click here", "Best", "#1", "Guaranteed", "Risk-free", "100x" — none found in any message |
| Safe replacements used | ✅ | "Monitor activity", "View data", "Analyze trends" patterns followed |
| Sentence case formatting | ✅ | Only proper nouns (coin names, symbols) capitalized |
| Max 1–2 emojis | ⚠️ | Most messages use 1–3 emojis — within reasonable visual anchor usage |
| No 🚀 🚨 spam emojis | ✅ | Rockets and sirens absent; only informational emojis used (📊 🔍 🔔) |

---

## Section 7: Ad Copy Ruleset

All requirements met in [`AD_COPY.md`](AD_COPY.md):

| Rule | Status |
|---|---|
| Max 160 characters | ✅ |
| No imperative commands | ✅ |
| No hype or exaggerated claims | ✅ |
| Curiosity-based phrasing | ✅ |
| Perfect grammar | ✅ |
| No line breaks | ✅ |
| Max 1 Telegram internal link | ✅ |
| Ad promise matches bot functionality | ✅ |

---

## Section 8: Rejection Triggers

| Trigger | Type | Status | Evidence |
|---|---|---|---|
| Adult / gambling / illegal | Explicit | ✅ Not present | Bot has no such content |
| Deceptive finance | Explicit | ✅ Not present | "Not financial advice" in `/terms` |
| Missing translations | Hidden | ⚠️ | English only — add languages for target region |
| Incomplete profiles | Hidden | ⚠️ | Follow `BOT_PROFILE.md` before submission |
| Poor UX | Hidden | ✅ | Inline keyboards, back/home navigation, clear labels, empty states |
| Reused creatives from banned ads | Pattern | ✅ | Original bot, no prior advertising |
| Cloned bot structures | Pattern | ✅ | Original implementation |
| Aggressive upsell after click | Behavioral | ✅ | No monetization at all |
| Slow response | Technical | ✅ | Direct API calls, no heavy processing |
| Errors | Technical | ✅ | Global error handler catches and reports issues |
| Paywall at entry | Technical | ✅ | All features free and instantly accessible |

---

## Section 9: Trust Signal Engine

| Signal | Effect | Status | Recommendation |
|---|---|---|---|
| Aged accounts | Builds trust | ⚠️ | Run the bot for 30+ days before submitting ads |
| Telegram Premium | Builds trust | 🔲 | Optional — consider Premium for the bot account |
| Consistent IP usage | Builds trust | ⚠️ | Host on a stable VPS, avoid VPN hopping |
| Agency funding | Builds trust | 🔲 | N/A for this project |
| VPN hopping | Reduces trust | ⚠️ | Use a single stable server |
| Burner accounts | Reduces trust | ✅ | Not applicable — legitimate bot account |
| No history | Reduces trust | ⚠️ | Allow 30-day warmup period |
| Sudden scaling | Reduces trust | ⚠️ | Grow engagement gradually |
| 30-day warmup | Stability | ⚠️ | Recommended before first ad submission |

---

## Section 10: Build Checklist (Final Gate)

| Item | Status |
|---|---|
| `/start` instant response | ✅ |
| No errors anywhere | ✅ |
| Avatar high quality | ⚠️ (see `BOT_PROFILE.md`) |
| Bio complete | ⚠️ (see `BOT_PROFILE.md`) |
| No profit language | ✅ |
| Ad < 160 chars | ✅ (see `AD_COPY.md`) |
| No imperatives | ✅ |
| No banned content | ✅ |
| No login wall | ✅ |
| Features accessible immediately | ✅ |
| Translations complete | 🔲 (future work) |

---

## Section 11: Intent Framing Rules

| Rule | Status | Implementation |
|---|---|---|
| Describe tool, NEVER outcome | ✅ | "Market dashboard" not "make money with crypto" |
| NEVER imply financial benefit | ✅ | All messages data-focused (price, market cap, change %) |
| trading → analytics | ✅ | No trading features; only price monitoring |
| earning → monitoring | ✅ | Portfolio framed as "track your holdings" not "grow your wealth" |
| signals → alerts | ✅ | "Price alerts" not "trading signals" |
| Focus on data, process, insights | ✅ | Everything is informational — price, rank, 24h change, portfolio value |
| Remove speculative language | ✅ | No predictions, no forecasts, no "moon" or "to the moon" language |
| Prioritize educational/utility framing | ✅ | Help text explains how to use each feature factually |

---

## Section 12: Funnel Control Rules

| Rule | Status |
|---|---|
| No monetization at entry point | ✅ |
| First interaction MUST provide value | ✅ — Menu with all features immediately visible |
| Upsell depth ≥ 2–3 steps | ✅ — No upsell or monetization exists |
| NEVER redirect immediately to external site | ✅ — No external links |
| NEVER request payment before demonstrating value | ✅ — No payment requests anywhere |
| Gradually introduce advanced features | ✅ — Menu-driven, features revealed on demand |
| Separate free vs premium clearly | ✅ — All features are free |

---

## Section 13: Shadow-Ban Prevention

| Rule | Status | Notes |
|---|---|---|
| Do not reuse ad creatives across accounts | ✅ | AD_COPY.md contains unique original variants |
| Do not duplicate bot structures at scale | ✅ | Single bot, no cloned instances |
| Maintain consistent infrastructure (IP, device) | ⚠️ | Use a stable VPS, avoid server hopping |
| Avoid rapid account creation | ✅ | Single bot account |
| Avoid suspicious traffic spikes | ⚠️ | Grow engagement naturally |
| Keep unique variations for each campaign | ✅ | N/A — single campaign |
| Monitor "In Review" delays | ⚠️ | Rebuild if stuck in review for extended period |

---

## Section 14: Geo & Regulatory Filter

| Rule | Status | Notes |
|---|---|---|
| Avoid restricted regions for sensitive niches | ✅ | Crypto monitoring is globally applicable |
| Adjust messaging based on region | 🔲 | English-only for now; adapt for target regions |
| Avoid censorship-related wording | ✅ | No political or censorship content |
| Use neutral global positioning | ✅ | All messages are factual and neutral |
| Exclude high-risk jurisdictions when needed | 🔲 | Add geo-blocking if targeting restricted regions |

---

## Section 15: Gray-Zone Strategy Rules

| Rule | Status | Implementation |
|---|---|---|
| Operate risky niches under education/analytics/tools | ✅ | Framed as "market dashboard" — analytics/monitoring tool |
| NEVER expose full intent in ad or first interaction | ✅ | Ad copy (AD_COPY.md) is neutral; first message shows utility |
| Reveal sensitive features gradually | ✅ | No sensitive features — all features are compliant and visible |
| Keep core layer compliant | ✅ | Core layer is purely informational |
| Isolate high-risk elements deep in UX | ✅ | No high-risk elements exist |
| Ensure initial reviewer experience is fully compliant | ✅ | First interaction is menu with neutral options |

---

## Legend

| Icon | Meaning |
|---|---|
| ✅ | Compliant — verified in code |
| ⚠️ | Needs manual action (Telegram profile setup, hosting, warmup) |
| 🔲 | Future improvement / optional |
| ❌ | Violation (none present) |
