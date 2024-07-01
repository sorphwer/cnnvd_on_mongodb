#use this file to load xml file into mongodb
#notes: the data in official cnnvd is not well-formed, so we have to do escaping.
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import xmltodict


uri = "your-mongodb-url"
xmlfiles = [
    # '2013.xml',
    '2014.xml',
    '2015.xml',
    '2016.xml',
    '2017.xml',
    '2018.xml',
    '2019.xml',
    '2020.xml',
    '2021.xml',
    '2022.xml',
    '2023.xml',
]
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
          

def loadXML(filename):
    with open(filename, encoding='utf-8') as f:
        xml = f.read()

    xml_lines = xml.split('\n')

    escaped_lines = []
    for line in xml_lines:
        l = []
        for i in range(0,len(line)):
            if line[i] == '&' or line[i] == '<' or line[i] == '>':
                l.append(i)
        if len(l)>4:
            for j in l[2:-2]:
                escaped_line = line[:l[1]+1] + line[l[1]+1:l[-2]].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;") + line[l[-2]:]
        else:
            escaped_lines.append(line)

    xml = '\n'.join(escaped_lines)
    cnnvd_obj = xmltodict.parse(xml)
    database = client['xml']
    collection = database['cnnvd']
    collection.insert_many(cnnvd_obj['cnnvd']['entry'])
    print(filename,'done')
for file in xmlfiles:
    loadXML(file)
