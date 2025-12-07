import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

Product_URL = "https://www.amazon.com/Apple-Version-Orange-Unlocked-Renewed/dp/B0FTC2PRVZ/ref=mp_s_a_1_3?crid=12DU2W23NGUG6&dib=eyJ2IjoiMSJ9.GyiR0GcyN_tVX_yq3UHqDHSsfvKHHipt_aXtlfqAbuLAIApqsYWEOJrlXC8YgKT2U2oflmiHUMRRBM13CnJCq1jPBl8eHdakCgv4UFERp6RQlZk0x9cm4bp0MLfPcTHLNK1RAtVT67uM_W05Ttdfm5DL5YXmpHlBLsAhQCJ5MgWQRC9posVq_wNTSSqiMQBEOyrZbiTAp7lV-FsHRd1Xgw.mYf6M63S7Hoq-FcR-xtNBYOJdv5j-1s71GnP9vAZn7o&dib_tag=se&keywords=iphone%2B17%2Bpro%2Bmax&qid=1764770796&sprefix=Iphone%2B1%2Caps%2C190&sr=8-3&th=1"
TARGET_PRICE = 1100
Price_History_File= "PriceHistory.csv"

FROM_EMAIL = os.getenv("FROM_EMAIL", "sherryliang38@gmail.com")
From_Name = os.getenv("FROM_NAME", "Amazon")
FROM_PASSWORD = os.getenv("FROM_PASSWORD", "gsqu mrca gmaa ysdf")
TO_EMAIL = os.getenv("TO_EMAIL", "21wilson.zhu@gmail.com")

def get_page_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

def parse_price_and_title(html: str) -> tuple[str | None, str | None]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else None

    price = None
    offscreen = soup.find("span", class_="a-offscreen")
    if offscreen:
        price_text = offscreen.get_text(strip=True)
        if price_text and price_text[0] == '$':
            price = price_text.split()[0]

    if not price:
        for pid in ["priceblock_ourprice", "priceblock_dealprice", "priceblock_saleprice",
                    "corePriceDisplay_desktop_feature_div"]:
            tag = soup.find(id=pid)
            if tag and tag.get_text(strip=True):
                price = tag.get_text(strip=True).split()[0]
                break

    return title, price

def extract_price_value(price_str: str) -> float | None:
    if not price_str:
        return None
    try:
        cleaned = price_str.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except ValueError:
        return None

def append_to_csv(timestamp: str, title: str | None, price: str | None, url: str, filename: str = "price_history.csv") -> None:
    path = Path(filename)
    file_exists = path.is_file()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "title", "price", "url"])
        writer.writerow([timestamp, title or "", price or "", url])

def send_email(subject: str, body: str) -> None:
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✓ Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("✗ Email error: Authentication failed.")
        print("  For Gmail with 2FA: Use an App Password instead of your regular password")
        print("  See: https://support.google.com/accounts/answer/185833")
    except smtplib.SMTPException as e:
        print(f"✗ Email error: {e}")
    except Exception as e:
        print(f"✗ Email error: {e}")


def track_product(url: str) -> None:
    try:
        html = get_page_html(url)
        title, price = parse_price_and_title(html)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("===================================")
        print(f"Checked at: {timestamp}")
        print(f"Product Name: {title if title else 'could not be found'}")
        print(f"Price: {price if price else 'could not be found'}")
        print("===================================")

        append_to_csv(timestamp, title, price, url, Price_History_File)

        Price_value = None
        if title and price:
            price_value = extract_price_value(price)

        email_subject = f"Price Update: {title}"
        email_body = (
            f"Product: {title}\n"
            f"Price: {price}\n"
            f"Target Price: ${TARGET_PRICE}\n"
            f"Checked at: {timestamp}\n"
            f"URL: {url}"
        )

        if price_value is not None and price_value <= TARGET_PRICE:
            email_subject = f"PRICE ALERT: {title} - PRICE HIT TARGET!"
            email_body = (
            "🎉 Great news! The price has dropped to your target!\n\n"
            f"Product: {title}\n"
            f"Current Price: {price}\n"
            f"Target Price: ${TARGET_PRICE}\n"
            f"Savings: ${TARGET_PRICE - price_value:.2f}\n\n"
            f"Checked at: {timestamp}\n"
            f"URL: {url}"
            )
            print(
                f"\n PRICE ALERT! Current price ({price}) "
                f"is at or below target (${TARGET_PRICE})!\n"
            )

        send_email(email_subject, email_body)

    except requests.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    track_product(Product_URL)

if __name__ == "__main__":
    main()







