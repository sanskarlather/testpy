from tkinter import PhotoImage
from extraction_func import *
feat_N = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                      'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic', 
                      'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards', 'Label']
# ─── DATA COLLECTION ────────────────────────────────────────────────────────────
Url = 'http://data.phishtank.com/data/online-valid.csv.gz'
wget.download(Url)
data_V = p.read_csv("online-valid.csv")
print(data_V.head())
data_B = p.read_csv("Benign_list_big_final.csv")
data_B.columns =['URLs']
print(data_B.head())

# ─── DATA SAMPLING ──────────────────────────────────────────────────────────────

url_P = data_V.sample(n=5000, random_state=12).copy()
url_P = url_P.reset_index(drop=True)
print(url_P.head())
print(url_P.shape)
url_L = data_B.sample(n=5000, random_state=12).copy()
url_L = url_L.reset_index(drop=True)
print(url_L.head())
print(url_L.shape)
# ────────────────────────────────────────────────────────────────────────────────

# ─── EXTRACTING FEATURES ────────────────────────────────────────────────────────

def featureExtraction(url,label):

  features = []
  #Address bar based features (10)
  features.append(ext_Dom(url))
  features.append(ext_IP(url))
  features.append(ext_AT(url))
  features.append(ext_Len(url))
  features.append(ext_Dep(url))
  features.append(ext_Red(url))
  features.append(ext_HTTP(url))
  features.append(ext_TU(url))
  features.append(ext_PreSuf(url))
  
  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(dns)
  features.append(ext_Rank(url))
  features.append(1 if dns == 1 else ext_Age(domain_name))
  features.append(1 if dns == 1 else domainEnd(domain_name))
  
  # HTML & Javascript based features (4)
  try:
    response = requests.get(url)
  except:
    response = ""
  features.append(ext_Frame(response))
  features.append(ext_SB(response))
  features.append(ext_RC(response))
  features.append(ext_For(response))
  features.append(label)
  
  return features

print(url_L.shape)

feat_L=[]
label=0
for i in range (0,10):
    url=url_L['URLs'][i]
    feat_L.append(featureExtraction(url,label))


legi=p.DataFrame(feat_L,columns=feat_N)
legi.head
legi.to_csv('legi.csv', index=False)
print(legi.head())

url_P.shape
feat_P=[]
label=1
for i in range(0,10):
  url=url_P['url'][i]
  feat_P.append(featureExtraction(url,label))
phisi=p.DataFrame(feat_P, columns= feat_N)
phisi.to_csv('phishisng.csv', index =False)

url_D=p.concat([legi,phisi]).reset_index(drop=True)
url_D.head()
url_D.tail()
url_D.shape
url_D.to_csv('urldata.csv',index=False)






