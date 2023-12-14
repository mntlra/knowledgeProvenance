import rdflib
from collections import defaultdict
import pandas as pd

from CoreNanopub.utils import _extractGCSID

GCS_QUERY = "PREFIX ceonto: <http://gda.dei.unipd.it/cecore/ontology/> " \
             "SELECT ?id ?involves ?hasType ?expressedBy ?CCSNotInformativeLikelihood ?PTNotInformativeLikelihood " \
             "?EGRActiveLikelihood ?EGRPassiveLikelihood ?AGTOncogeneLikelihood ?AGTTSGLikelihood" \
             " WHERE {" \
             "?id a ceonto:GCS;" \
             "ceonto:involves ?involves;" \
             "ceonto:hasType ?hasType;" \
             "ceonto:expressedBy ?expressedBy;" \
             "ceonto:CCSNotInformativeLikelihood ?CCSNotInformativeLikelihood;" \
             "ceonto:PTNotInformativeLikelihood ?PTNotInformativeLikelihood;" \
             "ceonto:EGRActiveLikelihood ?EGRActiveLikelihood;" \
             "ceonto:EGRPassiveLikelihood ?EGRPassiveLikelihood;" \
             "ceonto:AGTOncogeneLikelihood ?AGTOncogeneLikelihood;" \
             "ceonto:AGTTSGLikelihood ?AGTTSGLikelihood. }"

SENTENCE_QUERY = "PREFIX ceonto: <http://gda.dei.unipd.it/cecore/ontology/> " \
                 "PREFIX SIO: <http://semanticscience.org/resource/SIO_> " \
                 "SELECT ?sentence_id ?CCSLabel ?CELabel ?CGELabel ?PTLabel" \
                 " WHERE {" \
                 "?sentence_id a SIO:000113;" \
                 "ceonto:CCSLabel ?CCSLabel;" \
                 "ceonto:CELabel ?CELabel;" \
                 "ceonto:CGELabel ?CGELabel;" \
                 "ceonto:PTLabel ?PTLabel. }"

GCS_SENTENCE_QUERY = "PREFIX ceonto: <http://gda.dei.unipd.it/cecore/ontology/> " \
                     "SELECT ?gcs ?sentence" \
                     " WHERE {" \
                     "?gcs a ceonto:GCS;" \
                     "ceonto:supportedBy ?sentence." \



def extract_facts(dump, logger):
    logger.info(f"...Executing the query")
    # issue sparql query
    resultSet = dump.query(query_object=GCS_QUERY)
    logger.info(f"...Converting the query into a DataFrame")
    # convert query output to DataFrame
    gcs_dict = defaultdict(list)
    for row in resultSet:
        # store gcs URI
        gcs_dict['id'].append(str(row.id))
        # store additional information associated w/ GCS
        gcs_dict['involves'].append(str(row.involves))
        gcs_dict['hasType'].append(str(row.hasType))
        gcs_dict['expressedBy'].append(str(row.expressedBy))
        gcs_dict['CCSNotInformativeLikelihood'].append(str(row.CCSNotInformativeLikelihood))
        gcs_dict['PTNotInformativeLikelihood'].append(str(row.PTNotInformativeLikelihood))
        gcs_dict['EGRActiveLikelihood'].append(str(row.EGRActiveLikelihood))
        gcs_dict['EGRPassiveLikelihood'].append(str(row.EGRPassiveLikelihood))
        gcs_dict['AGTOncogeneLikelihood'].append(str(row.AGTOncogeneLikelihood))
        gcs_dict['AGTTSGLikelihood'].append(str(row.AGTTSGLikelihood))
    gcs = pd.DataFrame(gcs_dict)
    gcs["gcs_uri"] = gcs["id"]
    gcs["id"] = gcs["id"].apply(_extractGCSID)
    return gcs


def extract_sentences(dump, logger):
    logger.info(f"...Executing the query")
    # issue sparql query
    resultSet = dump.query(query_object=SENTENCE_QUERY)
    sentence2class = {}
    for row in resultSet:
        # store the sentence URI
        sentence_uri = row.sentence_id
        # classify the sentence
        gene_class = None
        # ?sentence_id ?CCSLabel ?CELabel ?CGELabel ?PTLabel
        if row.PTLabel != 'NOTINF':
            # update EGR
            if row.PTLabel == 'OBSERVATION':
                # sentence supports a passive role for target gene (i.e., BIOMARKER)
                gene_class = "BIOMARKER"

        if row.PTLabel == 'CAUSALITY' and row.CCSLabel != 'NOTINF':
            # sentence supports an active role for target gene
            if (row.CGELabel == 'UP' and row.CCSLabel == 'PROGRESSION') or \
                    (row.CGELabel == 'DOWN' and row.CCSLabel == 'REGRESSION'):
                # ONCOGENE
                gene_class = "ONCOGENE"
            if (row.CGELabel == 'DOWN' and row.CCSLabel == 'PROGRESSION') or \
                    (row.CGELabel == 'UP' and row.CCSLabel == 'REGRESSION'):
                # TSG
                gene_class = "TSG"

        # store the sentence class
        sentence2class[sentence_uri] = gene_class
    return sentence2class


def extract_gcs_sentence(dump, logger):
    logger.info(f"...Executing the query")
    # issue sparql query
    resultSet = dump.query(query_object=GCS_SENTENCE_QUERY)
    logger.info(f"...Converting the query into a DataFrame")
    # convert query output to DataFrame
    gcs_sentence_dict = defaultdict(list)
    for row in resultSet:
        # store gcs URI
        gcs_sentence_dict['gcs'].append(str(row.gcs))
        # store sentence associated w/ GCS
        gcs_sentence_dict['sentence'].append(str(row.sentence))

    gcs_sentence = pd.DataFrame(gcs_sentence_dict)
    logger.info(f"...Integrating sentences gene classes into the DataFrame")
    gcs_sentence["sentenceClass"] = gcs_sentence["sentence"].map(extract_sentences(dump, logger))
    return gcs_sentence

