""" 
This is a crawler program using beautifulsoup.
It crawls the website "https://sport050.nl/sportaanbieders/alle-aanbieders/"
and fetches all the sport suppliers in the city of Groningen. It outputs 
a csv-file with the url;phone-number;email-address of all the suppliers it can find.
"""

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re


def hack_ssl():
    """ ignores the certificate errors"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def open_url(url):
    """ reads url file as a big string and cleans the html file to make it
        more readable. input: url, output: soup object
    """
    ctx = hack_ssl()
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def read_hrefs(soup):
    """ get from soup object a list of anchor tags,
        get the href keys and and prints them. Input: soup object
    """
    reflist = []
    tags = soup('a')
    for tag in tags:
        reflist.append(tag)
    return reflist

def read_li(soup):
    lilist = []
    tags = soup('li')
    for tag in tags:
        lilist.append(tag)
    return lilist

def get_phone(info):
    reg = r"(?:(?:00|\+)?[0-9]{4})?(?:[ .-][0-9]{3}){1,5}"
    phone = [s for s in filter(lambda x: 'Telefoon' in str(x), info)]
    try:
        phone = str(phone[0])
    except:
        phone = [s for s in filter(lambda x: re.findall(reg, str(x)), info)]
        try:
            phone = str(phone[0])
        except:
            phone = ""   
    return phone.replace('Facebook', '').replace('Telefoon:', '')

def get_email(soup):
    try: 
        email = [s for s in filter(lambda x: '@' in str(x), soup)]
        email = str(email[0])[4:-5]
        bs = BeautifulSoup(email, features="html.parser")
        email = bs.find('a').attrs['href'].replace('mailto:', '')
    except:
        email = ""
    return email

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def fetch_sidebar(soup):
    """ reads html file as a big string and cleans the html file to make it
        more readable. input: html, output: tables
    """
    sidebar = soup.findAll(attrs={'class': 'sidebar'})
    return sidebar[0]

def extract(url):
    text = str(url)
    text = text[26:].split('"')[0] + "/"
    return text


print ('fetch urls')
url = "https://sport050.nl/sportaanbieders/alle-aanbieders/"
s = open_url(url)
reflist = read_hrefs(s)

print ('getting sub-urls')
sub_urls = [s for s in filter(lambda x: '<a href="/sportaanbieders' in str(x), reflist)]
sub_urls = sub_urls[3:]

print ('extracting the data')
print (f'{len(sub_urls)} sub-urls')

for sub in sub_urls:
    try:
        sub = extract(sub)
        site = url[:-16] + sub
        soup = open_url(site)    
        info = fetch_sidebar(soup)
        info = read_li(info)
        phone = get_phone(info)
        phone = remove_html_tags(phone).strip()
        email = get_email(info)
        email = remove_html_tags(email).replace("/","")
        print (f'{site} ; {phone} ; {email}')
    except Exception as e:
        print (e)
        exit()


class Crawler():
    def __init__(self, url):
        print ('fetch urls')
        self.url = url
        self.soup = self.open_url()
        self.sub_urls = self.sub_url_maker()


    def open_url(self):
        """ reads url file as a big string and cleans the html file to make it
            more readable. input: url, output: soup object
        """
        ctx = hack_ssl()
        html = urllib.request.urlopen(self.url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def sub_url_maker(self):
        reflist = read_hrefs(self.soup)
        print ('getting sub-urls')
        sub_urls = [s for s in filter(lambda x: '<a href="/sportaanbieders' in str(x), reflist)]
        sub_urls = sub_urls[3:]

        print ('extracting the data')
        print (f'{len(sub_urls)} sub-urls')

        return sub_urls

    def crawl_site(self):
        for sub in self.sub_urls:
            try:
                sub = extract(sub)
                site = url[:-16] + sub
                soup = open_url(site)    
                info = fetch_sidebar(soup)
                info = read_li(info)
                phone = get_phone(info)
                phone = remove_html_tags(phone).strip()
                email = get_email(info)
                email = remove_html_tags(email).replace("/","")
                print (f'{site} ; {phone} ; {email}')
            except Exception as e:
                print (e)
                exit()

    def extract(self, sub_url):
        text = str(sub_url)
        text = text[26:].split('"')[0] + "/"
        return text


    def open_url(self, site):
        """ reads url file as a big string and cleans the html file to make it
            more readable. input: url, output: soup object
        """
        ctx = hack_ssl()
        html = urllib.request.urlopen(site, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def fetch_sidebar(self, sub_soup):
        """ reads html file as a big string and cleans the html file to make it
            more readable. input: html, output: tables
        """
        sidebar = sub_soup.findAll(attrs={'class': 'sidebar'})
        return sidebar[0]

    def read_li(self, information):
        lilist = []
        tags = information('li')
        for tag in tags:
            lilist.append(tag)
        return lilist

    def get_phone(self, information):
        reg = r"(?:(?:00|\+)?[0-9]{4})?(?:[ .-][0-9]{3}){1,5}"
        phone = [s for s in filter(lambda x: 'Telefoon' in str(x), information)]
        try:
            phone = str(phone[0])
        except:
            phone = [s for s in filter(lambda x: re.findall(reg, str(x)), information)]
            try:
                phone = str(phone[0])
            except:
                phone = ""   
        return phone.replace('Facebook', '').replace('Telefoon:', '')

    @staticmethod
    def hack_ssl():
        """ ignores the certificate errors"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
