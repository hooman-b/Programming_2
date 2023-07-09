from multiprocessing import Process
from Bio import Entrez
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#enter your email here; the one you used to create an api key in step 0
Entrez.email = '' 

file = Entrez.elink(dbfrom="pubmed",
                   db="pmc",
                   LinkName="pubmed_pmc_refs",
                   id="30049270",
                   api_key='personal_API_key')
results = Entrez.read(file)
print (results)

##############################
references = [f'{link["Id"]}' for link in results[0]["LinkSetDb"][0]["Link"]]
print(references)
##############################
handle = Entrez.efetch(db="pubmed",
                       id='30049270',
                       retmode="xml",
                       api_key='personal_API_key')
print(handle.read())
##############################

def Download(id):
    handle = Entrez.efetch(db="pubmed",
                           id=id,
                           rettype="text",
                           retmode="xml",
                           api_key='personal_API_key')
    with open(f'{id}.xml', 'w') as f:
        f.write(str(handle.read()))
    print(f'{id} is now')

    # print(handle.read())
if __name__ == "__main__":
    procsessList = []
    for id in references[:10]:
        process = Process(target=Download, args=(id,))
        procsessList.append(process)
        process.start()
    for one_process in procsessList:
        one_process.join()