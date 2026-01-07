import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://rss.cnn.com/rss/edition.rss"

def get_top_headline() -> str:
    with urllib.request.urlopen(RSS_URL) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    for item in root.iter("item"):
        return item.find("title").text

    raise RuntimeError("No headlines found")
