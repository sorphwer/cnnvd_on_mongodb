from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import xmltodict
uri = "mongodburl"

query = 'nginx'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
cnnvds = client['xml']['cnnvd']

def get_pipeline(query):
    pipeline = [
        {
            '$search': {
                'index': 'cnnvd_search_index',
                'text': {
                    'query': 'TBD',
                    'path': 'name',
                    'fuzzy': {
                        'maxEdits': 2,
                        'prefixLength': 0,
                        'maxExpansions': 50
                    }
                }
            }
        },
        {
            '$project': {
                '_id': 0
            }
        },
        {
        '$sort': {
            'modified': -1 
        }
    }
    ]
    pipeline[0]['$search']['text']['query'] = query
    return pipeline


def format_result(result):
    formatted_result = f"""
    Name: {result.get('name')}
    Vulnerability ID: {result.get('vuln-id')}
    Published Date: {result.get('published')}
    Modified Date: {result.get('modified')}
    Severity: {result.get('severity')}
    Vulnerability Type: {result.get('vuln-type')}
    Description: {result.get('vuln-descript')}
    CVE ID: {result.get('other-id', {}).get('cve-id')}
    Solution: {result.get('vuln-solution')}
    """
    return formatted_result.strip()

try:
    client.admin.command('ping')
    print("DB Connected!")
except Exception as e:
    print(e)


results = list(cnnvds.aggregate(get_pipeline(query)))
print('Get',cnnvds.count_documents({}),'Records in total, Found ',len(results),'matches')
print('-' * 80) 
for result in results:
    print(format_result(result))
    print('-' * 80) 
