from subprocess import call
import requests
import json 
import pandas as pd 



def call_for_genes(protein_accession: list) -> dict:
    """Takes list of Uniprot protein accessions, returns hash map of gene names.
    
    :arg protein_accession: (list)  list of protein accession numbers

    :returns: json/dict
    """

    # join accessions
    accs = '%2C'.join(protein_accession)
    
    # include in url
    base_url = f'https://rest.uniprot.org/uniprotkb/accessions?accessions={accs}'
    
    # get response
    r = requests.get(base_url)

    # dump into json object
    resp = json.loads(r.text)
    return resp

def parse_response(uniprot_resp: dict):
    """Parses uniprot response.
    
    :arg unriprot_resp: (dict)  response from uniprot
    
    :returns:   {accession: gene}
    """
    
    # account for single searches
    if len(uniprot_resp) != 0:
        data = uniprot_resp["results"]
    else:
        data = uniprot_resp
    
    # keep track of results and misisng values
    lookup = {}
    count = 0

    for entry in data:
        # grab accession that was passed in
        val = entry['primaryAccession']
        
        # some accessions do not have associated genes
        try:
            found_gene = entry["genes"][0]['geneName']["value"]
        except:
            found_gene = None
            count += 1
        
        # add gene to map
        lookup[val] = found_gene
    
    # provide warning
    if count > 0:
        print(f'{count} protein accessions were not mapped!')

    return lookup


if __name__ == '__main__':


    data = pd.read_csv(r"C:\Users\graha\Downloads\uniprot-download_true_fields_accession_2Cid_2Cprotein_name_format_ts-2022.08.17-23.06.33.39.tsv", delimiter='\t')
    test_accs = data['Entry'][:1].tolist()
    
    c = call_for_genes(test_accs)
    m = parse_response(c)
    print(m)

    