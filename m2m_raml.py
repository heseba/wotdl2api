#DEPRECATED

import yaml
import rdflib
from rdflib import OWL, RDFS, Namespace
from urllib.parse import urlparse
from collections import defaultdict

VSR = Namespace('http://www.tu-chemnitz.de/vsr/ontology#')

instance = rdflib.Graph()
instance.parse('../sample.ttl', format='n3')

find_http_requests = """SELECT ?d ?device ?http_request ?name ?method ?url
       WHERE {
            ?d a ?device_subclass.
            ?device_subclass a owl:Class.
            ?device_subclass rdfs:subClassOf vsr:Device.
            OPTIONAL{ ?d vsr:name ?device }
            ?http_request a vsr:HttpRequest .
            OPTIONAL{?http_request vsr:name ?name}
            ?http_request vsr:httpMethod ?method .
            ?http_request vsr:url ?url . 
            {
                ?d vsr:hasTransition ?t.
                ?t vsr:hasActuation ?http_request.
            } 
            UNION 
            { 
                ?d vsr:hasMeasurement ?http_request.                          
            }
        }
"""

#TODOs Mahda:
#Sensor1 missing name
#BaseURI missing
#URLs are inconsistent (10.0.1.113 and 10.1.13.14)
#Mime types and Message formats are missing in Ontology


raml = {
    'title': '',
    'baseUri': 'https://localhost:80/api',
    'version': 'v1',
}

http_requests = instance.query(find_http_requests, initNs={'vsr': VSR, 'rdfs': RDFS, 'owl': OWL})
resources = defaultdict(list)

for device, devicename, http_request, name, method, url in http_requests:
    print('%s %s %s %s %s' % (device, http_request, name, method, url))
    url = urlparse(url)
    resources[url.path].append({'method': method, 'device': devicename, 'name': name, 'query_params': url.query})




for resource in resources:
    requests = resources[resource]

    for request in requests:
        entry = {}
        current = raml
        resource_parts = resource.split('/')
        for part in resource_parts[1:-1]:
            if not '/' + part in current:
                current['/' + part] = {}
            current = current['/' + part]
        leaf = resource_parts[-1]
        entry[str(request['method'])] = {
            'description': "%s" % request['name'],
            'responses': [],
        }
        if request['query_params'] != '':
            entry[str(request['method'])]['queryParameters'] = {
                request['query_params'].split('=')[0]: {
                    'example': request['query_params'].split('=')[1]
                }
            }
        current['/' + leaf] = entry


with open('../api.raml', 'w') as yamlfile:
    yamlfile.write('#%RAML 0.8')
    yaml.dump(raml, stream=yamlfile)