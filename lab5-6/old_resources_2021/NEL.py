from collections import defaultdict
import requests
import spotlight
import wikipedia


ma = wikipedia.WikipediaPage(title='Marcus Aurelius').content
# This ensures that all returns in general should only give us valid fields in the last part :^D 📈
only_person_filter = {
    'policy': "whitelist",
    'types': "DBpedia:Person",
    'coreferenceResolution': False
}

# The values for the confidence and the support makes it so that you might actually miss peoepl that you'd find if you used say Spacy with TRF to find entities and the linked them with Annotate afterwards.
# i.e this might not be the optimal solution.
annotations = spotlight.annotate(
    'https://api.dbpedia-spotlight.org/en/annotate', ma, confidence=0.8, support=10, filters=only_person_filter)

# Filter for people

people = list(set([annotation["URI"].split("/")[-1]
                   for annotation in annotations]))[:5]
f"http://vmdbpedia.informatik.uni-leipzig.de:8080/api/1.0.0/values?entities=Marcus_Aurelius%2CAugustus%2CSohaemus_of_Armenia%2CZeno_of_Citium%2CPliny_the_Younger&property=dbp%3AbirthPlace&property=dbp%3AbirthName&pretty=NONE&limit=100&offset=0&key=1234&oldVersion=false"

people_string = ",".join(people)
properties = ["dbp:birthName", "dbp:birthPlace"]
# i cannot be bothered to use the proper pythonic way, list comp, map or reduce :S, either one should be prettier than this 🚀
propertyString = ""
for prop in properties:
    propertyString += f"property={prop}&"

URL = f"http://vmdbpedia.informatik.uni-leipzig.de:8080/api/1.0.0/values?entities={people_string}&{propertyString}pretty=NONE&limit=100&offset=0&key=1234&oldVersion=true"
data = requests.get(URL,
                    headers={
                        "Accept": "application/json"
                    },).json()
bindings = data.get("results").get("bindings")
# This should be an unpack funtion, and not written as a pure map, hard to read 😅
results = list(map(lambda res: [res["entities"]["value"].split(
    "/")[-1], res.get("dbpbirthName", {}).get("value", {}), res.get("dbpbirthPlace", {}).get("value", {})], bindings))
# Should use Tabulate
print(results)
