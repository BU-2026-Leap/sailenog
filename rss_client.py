import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://news.google.com/rss/search?q=site:cnn.com&hl=en-US&gl=US&ceid=US:en"

def get_top_headline() -> str:
    with urllib.request.urlopen(RSS_URL) as response:
        xml_data = response.read()

        root = ET.fromstring(xml_data)
        first_title = root.find("channel").find("item")[0]

        return first_title.text



    raise RuntimeError("No headlines found")

