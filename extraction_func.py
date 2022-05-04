import imp
import ipaddress
import re
import urllib
import urllib.request
from datetime import datetime
from fileinput import filename
from urllib.parse import urlencode, urlparse

import pandas as p
import requests
import wget
import whois
from bs4 import BeautifulSoup
from matplotlib.collections import Collection


url_Short = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"



def ext_Dom(url):
    dom= urlparse(url).netloc
    if re.match(r"^www.",dom):
        dom=dom.replace("www.","")
        print("Domain Extraction of url succesful")
        print(dom)
        return dom

def ext_IP(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    print()
    return ip

def ext_AT(url):
  if "@" in url:
    at = 1    
  else:
    at = 0    
  return at


def ext_Len(url):
  if len(url) < 54:
    length = 0            
  else:
    length = 1            
  return length


def ext_Dep(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

def ext_Red(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0


def ext_HTTP(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0

def ext_TU(url):
    match=re.search(url_Short,url)
    if match:
        return 1
    else:
        return 0


def ext_PreSuf(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate

def ext_Rank(url):
  try:
    
    url = urllib.parse.quote(url)
    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
        "REACH")['RANK']
    rank = int(rank)
  except TypeError:
        return 1
  if rank <100000:
    return 1
  else:
    return 0



def ext_Age(domain_name):
  date_CR = domain_name.creation_date
  date_EX = domain_name.expiration_date
  if (isinstance(date_CR,str) or isinstance( date_EX,str)):
    try:
      date_CR = datetime.strptime(date_CR,'%Y-%m-%d')
      expiration_date = datetime.strptime( date_EX,"%Y-%m-%d")
    except:
      return 1
  if (( date_EX is None) or (date_CR is None)):
      return 1
  elif ((type( date_EX) is list) or (type(date_CR) is list)):
      return 1
  else:
    ageofdomain = abs(( date_EX - date_CR).days)
    if ((ageofdomain/30) < 6):
      age = 1
    else:
      age = 0
  return age

def domainEnd(domain_name):
  date_EX = domain_name.expiration_date
  if isinstance(date_EX,str):
    try:
      date_EX = datetime.strptime(date_EX,"%Y-%m-%d")
    except:
      return 1
  if (date_EX is None):
      return 1
  elif (type(date_EX) is list):
      return 1
  else:
    today = datetime.now()
    end = abs((date_EX - today).days)
    if ((end/30) < 6):
      end = 0
    else:
      end = 1
  return end


def ext_Frame(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 0
      else:
          return 1

def ext_SB(response): 
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 1
    else:
      return 0

def ext_RC(response):
  if response == "":
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return 0
    else:
      return 1
  
def ext_For(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1


