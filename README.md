# OPTCG-Price-Tracker
A price aggregation algorithm for One Piece TCG cards — normalising multi-language (JPN/ENG/CHN) and multi-condition (raw/graded) prices across global market platforms into a single reliable market reference

---

# The Problem
Tracking the fair market price of an OPTCG card is surprisingly difficult, with all the different available platforms online, and prices are all scattered inconsistently. More critically, there are three layers of incomparability that determines different card prices:

**1. Language versions are different products**
The same card exists in Japanese, English, and Chinese — and 
each language version carries a completely different market 
price. They should never be directly compared.

**2. Raw vs graded cards are different products**
A raw Near Mint card and a PSA 10 slab of the same card exist 
in entirely separate markets with very different price ranges.

**3. Grading company affects slab value**
A PSA 10, CGC 10, and BGS 10 of the same card are not priced 
equivalently — the grading company is part of the product.

---

## What This Algorithm Does

- Scrapes real-time card prices from key platforms per language:
  - JPN → Yuyutei (retail benchmark), Mercari Japan 
          (secondhand/transaction prices)
  - ENG → TCGPlayer (primary), PriceCharting (historical trends)
  - CHN → (platform TBD)
- Tracks slab prices separately by grading company 
  (PSA / CGC / BGS) and grade
- Treats language, condition, and grader as core attributes — 
  never mixing incomparable prices
- Converts all currencies to a unified reference (SGD / USD) 
  using live exchange rates
- Normalises card condition standards across platforms 
  (NM / LP / MP / HP)
- Builds a canonical card identity system based on official 
  OPTCG card numbers (e.g. OP01-001) as the unique identifier
- Tracks price history over time as data accumulates daily
- Detects anomalies — post-tournament spikes, reprint 
  announcements, sudden market shifts
- Outputs a fair market value estimate per card, per language, 
  per condition — clearly separated, never conflated

---

## Data Model

Every price entry in this algorithm is identified by:

    Card Number  : OP01-001          (official OPTCG card number)
    Language     : JPN / ENG / CHN   (never mixed)
    Type         : Raw / Graded      (never mixed)
    Grader       : PSA / CGC / BGS   (graded cards only)
    Grade        : 10 / 9.5 / 9 ... (graded cards only)
    Platform     : Yuyutei / TCGPlayer / etc.
    Price (local): ¥800
    Price (SGD)  : ~$7.20
    Date         : 2026-05-25



