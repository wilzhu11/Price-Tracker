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





