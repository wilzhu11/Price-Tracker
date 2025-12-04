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
TARGET_PRICE = 1200.00

From_Email = os.getenv("FROM_EMAIL", "sherryliang38@gmail.com")
From_Name = os.getenv("FROM_NAME", "AMAZON")
FROM_Password = os.getenv("FROM_PASSWORD", "gsqu mrca gmaa ysdf")
To_Email = os.getenv("TO_EMAIL", "21wilson.zhu@gmail.com")

def get_page_html(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

def parse_price_and_title(html: str) -> tuple[str,None, str, None]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else None

    for pid in price_ids:
        tag = soup.find(id=pid)
        if tag:
            price_text = tag.get_text(strip=True)
            if price_text:
                price = price_text.split()[0]
                break


price = None
for pid in ["priceblock_ourprice", "priceblock_dealprice", "priceblock_saleprice",
            "corePriceDisplay_desktop_feature_div"]:
    tag = soup.find(id=pid)
    if tag and tag.get_text(strip=True):
        price = tag.get_text(strip=True).split()[0]
        break

if not price:
    offscreen = soup.find("span", class_="a-offscreen")
    if offscreen:
        price = offscreen.get_text(strip=True).split()[0] if offscreen.get_text(strip=True) else None

    return title, price


def parse_price_and_title(html: str) -> tuple[str | None, str | None]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else None

    price = None
    for pid in ["priceblock_ourprice", "priceblock_dealprice", "priceblock_saleprice",
                "corePriceDisplay_desktop_feature_div"]:
        tag = soup.find(id=pid)
        if tag and tag.get_text(strip=True):
            price = tag.get_text(strip=True).split()[0]
            break

    if not price:
        offscreen = soup.find("span", class_="a-offscreen")
        if offscreen:
            price = offscreen.get_text(strip=True).split()[0] if offscreen.get_text(strip=True) else None

    return title, price

def extract_price_value(price_str: str) -> float | None:
    """Convert price string to float"""
    if not price_str:
        return None
    try:
        cleaned = price_str.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except ValueError:
        return None









