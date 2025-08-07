import json, time 
import os, hashlib, requests
from bs4 import BeautifulSoup

BASE_URL= "https://youmed.vn/tin-tuc/duoc/"
OUTPUT_DIR = "data/medicines"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw.json")