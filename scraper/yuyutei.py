import requests
from bs4 import BeautifulSoup
from datetime import date

def scrape_yuyutei(card_number):

    url = f"https://yuyu-tei.jp/sell/opc/s/search?search_word={card_number}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"\nSearching Yuyutei for: {card_number}")
    print(f"URL: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to reach Yuyutei. Status code: {response.status_code}")
        return []

    print("Successfully reached Yuyutei!")

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    sections = soup.find_all("div", class_="py-4")

    if not sections:
        print("No sections found — page structure may have changed")
        return []

    for section in sections:

        variant_badge = section.find("span", class_=lambda c: c and "text-white" in c)
        if variant_badge:
            variant = variant_badge.get_text(strip=True)
        else:
            variant = "REG"

        card_listings = section.find_all("div", class_="card-product")

        if not card_listings:
            continue

        print(f"\nFound variant section: {variant} ({len(card_listings)} listing/s)")

        for i, card in enumerate(card_listings):

            card_num_tag = card.find(
                "span",
                class_=lambda c: c and "border-dark" in c
            )
            card_num = card_num_tag.get_text(strip=True) if card_num_tag else card_number

            name_tag = card.find(
                "a",
                href=lambda h: h and "/sell/opc/card/" in h if h else False
            )
            card_name = name_tag.get_text(strip=True) if name_tag else "Unknown"

            price_tag = card.find("strong", class_=lambda c: c and "text-end" in c)
            if price_tag:
                raw_price = price_tag.get_text(strip=True)
                price_jpy = raw_price.replace("円", "").replace(",", "").strip()
                try:
                    price_jpy = int(price_jpy)
                except ValueError:
                    price_jpy = None
            else:
                price_jpy = None

            if variant == "P-SEC" and len(card_listings) > 1:
                variant_label = f"P-SEC-{i+1}"
            else:
                variant_label = variant

            listing = {
                "card_number"    : card_num,
                "card_name"      : card_name,
                "source_variant" : variant,
                "variant"        : variant_label,
                "language"       : "JPN",
                "type"           : "Raw",
                "platform"       : "Yuyutei",
                "price_jpy"      : price_jpy,
                "date"           : str(date.today())
            }

            results.append(listing)
            print(f"  [{variant_label}] {card_name} | ¥{price_jpy:,}")

    return results


if __name__ == "__main__":
    card_number = input("Enter card number (e.g. OP13-118): ").strip().upper()
    results = scrape_yuyutei(card_number)

    print(f"\n{'='*50}")
    print(f"Total listings found for {card_number}: {len(results)}")
    print(f"{'='*50}")

    for r in results:
        print(r)