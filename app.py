"""This is a simple Flask API app to serve plain text data from the BioStudies API"""


import json
import requests
import datetime
from flask import Flask, request


def get_public_adfs_from_biostudies():

    """Generate list of accession and title from querying the public BioStudies API"""

    biostudies_base = "https://www.ebi.ac.uk/biostudies/api/v1/"
    api_query = "search?collection=arrayexpress&type=array"

    adfs = {}

    try:
        response = requests.get(biostudies_base + api_query)
        data = json.loads(response.text)

        total_hits = data.get("totalHits")
        #total_hits = 300  # limit for testing
        page_size = 100

        if total_hits and page_size:
            for i in range(1, int(int(total_hits) / int(page_size)) + 2):
                r = requests.get(biostudies_base + api_query + f"&pageSize={page_size}&page={i}")
                data = json.loads(r.text)
                for adf in data.get("hits", []):
                    adfs[adf["accession"]] = adf["title"]

    except Exception:
        print("Failed to get response from BioStudies API")

    return adfs


app = Flask(__name__)
adf_dict = get_public_adfs_from_biostudies()


@app.route('/arrays', methods=['GET'])
def lookup_adfs():
    """Call pre-generated ADF list and serve as text file"""

    global adf_dict

    # Filter by accession if parameter specified
    try:
        accession = request.args.get("acc")
        if accession:
            adf_info = f"1\t{accession}\t{adf_dict[accession]}\n"
            return adf_info, 200, {'Content-Type': 'text/css; charset=utf-8'}
    except KeyError:
        pass

    # Return full list
    adf_list = [f"{i}\t{adf[0]}\t{adf[1]}" for i, adf in enumerate(adf_dict.items())]
    return "\n".join(adf_list), 200, {'Content-Type': 'text/css; charset=utf-8'}


@app.route('/update_arrays', methods=['GET'])
def update_adfs():
    """Call function to generate ADF list"""

    global adf_dict

    adf_dict = get_public_adfs_from_biostudies()
    # [f"Generated at {datetime.datetime.now()}"] + \

    return "Successfully updated ADF list.", 201
