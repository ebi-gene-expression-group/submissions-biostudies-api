"""This is a simple Flask API app to serve plain text data from the BioStudies API"""

from flask import Flask, request

def get_public_adfs_from_biostudies():

    """Generate list of accession and title from querying the biostudies Array designs file"""

    arrays_data_file = "/nfs/production/irene/ma/annotare/biostudies/arrayexpress-arrays.txt"

    adfs = {}

    try:
        with open(arrays_data_file, "r") as file:
            for line in file:
                tokens = line.strip().split("\t")
                accession = tokens[0]
                title = tokens[3]
                adfs[accession] = title
    except Exception:
        print("Unable to read from arrays data file.")

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
