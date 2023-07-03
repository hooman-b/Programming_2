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

class Crawler():
    def __init__(self, url):
        print ('fetch urls')
        self.url = url
        self.soup = self.open_url(url)
        self.sub_urls = self.sub_url_maker()
        self.pointer = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.pointer += 1
        if self.pointer == len(self.sub_urls):
            raise StopIteration
        return self.sub_urls[self.pointer]

    def open_url(self, url):
        """ reads url file as a big string and cleans the html file to make it
            more readable. input: url, output: soup object
        """
        ctx = self.hack_ssl()
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def sub_url_maker(self):
        reflist = self.read_hrefs()
        print ('getting sub-urls')
        sub_urls = [s for s in reflist if '<a href="/sportaanbieders' in str(s)]
        sub_urls = sub_urls[3:]

        print ('extracting the data')
        print (f'{len(sub_urls)} sub-urls')

        return sub_urls

    def read_hrefs(self):
        """ get from soup object a list of anchor tags,
            get the href keys and and prints them. Input: soup object
        """
        reflist = []
        tags = self.soup('a')
        for tag in tags:
            reflist.append(tag)
        return reflist


    def crawl_site(self):
        for sub in self.sub_urls:
            try:
                sub = self.extract(sub)
                site = self.url[:-16] + sub
                soup = self.open_url(site)    
                info = self.fetch_sidebar(soup)
                info = self.read_li(info)
                phone = self.get_phone(info)
                phone = self.remove_html_tags(phone).strip()
                email = self.get_email(info)
                email = self.remove_html_tags(email).replace("/","")
                yield f'{site} ; {phone} ; {email}'
            except Exception as e:
                yield e
                exit()



    def extract(self, sub_url):
        text = str(sub_url)
        text = text[26:].split('"')[0] + "/"
        return text

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

        phone = [s for s in information if 'Telefoon' in str(s)]

        try:
            phone = str(phone[0])
        except:
            phone = [s for s in information if re.findall(reg, str(s))]

            try:
                phone = str(phone[0])
            except:
                phone = ""   
        return phone.replace('Facebook', '').replace('Telefoon:', '')

    def get_email(self, information):
        try:
            email = [s for s in information if '@' in str(s)]
            email = str(email[0])[4:-5]
            bs = BeautifulSoup(email, features="html.parser")
            email = bs.find('a').attrs['href'].replace('mailto:', '')
        except:
            email = ""
        return email

    @staticmethod
    def hack_ssl():
        """ ignores the certificate errors"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    @ staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)