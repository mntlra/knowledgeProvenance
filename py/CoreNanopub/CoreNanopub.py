import pandas as pd
from CommonNanopub.CommonNanopub import CommonNanopub
from rdflib import Namespace, ConjunctiveGraph

from .utils import _extractGCSID


class CoreNanopub(CommonNanopub):

    def __init__(self, path_to_properties='../properties/common.ini', sample=True):
        """
        Initialisation function.

        :param path_to_properties : (str) path to properties file.
        :param sample: (bool) whether to serialize a sample GCS facts or all GCS facts.
        """
        super().__init__()
        self.gcs_path = self.config["PATHS.DATASET.SAMPLE"]["gcs"] if sample else self.config["PATHS.DATASET"]["gcs"]
        self.gcs_sentence_path = self.config["PATHS.DATASET.SAMPLE"]["gcs_sentence"] if sample else \
            self.config["PATHS.DATASET"]["gcs_sentence"]

        self.serialization_formats = self.config["SERIALIZATION"]["formats"].split(",")
        serialization_prop = "PATHS.SERIALIZATION.SAMPLE" if sample else "PATHS.SERIALIZATION"
        self.serialization_path = {}
        for ser_format in self.serialization_formats:
            self.serialization_path[ser_format] = self.datadir + self.config[serialization_prop][ser_format]

    def read_data(self):
        """
        Read csv files into dataframes.

        :param self: self object.
        """

        self.gcs = pd.read_csv(self.datadir+self.gcs_path, index_col=False)
        self.gcs["gcs_uri"] = self.gcs["id"]
        # self.gcs["id"] = self.gcs["id"].apply(lambda x: x.lstrip("http://gda.dei.unipd.it/cecore/resource/GCS#"))
        self.gcs["id"] = self.gcs["id"].apply(_extractGCSID)
        self.gcs.set_index("id", inplace=True)
        self.gcs_sentence = pd.read_csv(self.datadir+self.gcs_sentence_path, index_col="id")

    def process_data(self):
        """
        Remove invalid GCS facts.
        """
        self.invalidGCS = self.process_gcs()
        # Drop invalid GCS
        original_len = len(self.gcs.index)
        self.gcs = self.gcs.loc[~self.gcs.index.isin(self.invalidGCS)]

        self.logger.info(f"Dropped {len(self.invalidGCS)} inconclusive GCS facts - "
                         f"{len(self.gcs.index)} GCS facts remaining (originally {original_len})")

    def get_namespaces(self, gcs_id):
        """
        Create a dictionary with ('namespace_id', URL) of each namespace defined in the property files.
        """
        self.namespaces = {nid: Namespace(uri) for nid, uri in self.config['NAMESPACES'].items()}
        # Add the considered extended_nanopub's namespaces
        self.namespaces["this"] = Namespace(self.namespaces["corenp"] + gcs_id)
        self.namespaces["sub"] = Namespace(self.namespaces["corenp"] + gcs_id + "#")

    def initializeFullGraph(self, identifier):
        """
        Initialize the graph and bind the namespaces.
        :param self: self object.
        :param identifier: (str) name of the graph.

        :return: self object, which is the updated graph.
        """
        # Get useful namespaces
        self.get_namespaces(identifier)
        # Create the named graph
        graph_name = self.namespaces["corenp"][identifier]
        self.nanopub_graph = ConjunctiveGraph(identifier=graph_name)

        return self

    def create_nanopub_graphs(self):
        """
        Iterate over the facts and create a extended_nanopub for each of them.
        :return: self object.
        """
        self.logger.info(f"--- Reading and Processing Data ---")
        self.read_data()
        self.process_data()
        self.logger.info(f"--- Reading and Processing COMPLETED ---")
        self.logger.info(f"+++ Start Nanopublications Serialization +++")
        self.current_serialized = 1
        self.to_be_serialized = len(self.gcs.index)
        self.gcs.apply(self._createNanopub, axis=1)
        return self

    from .core_nanopub_creation import _createNanopub, _populateAssertionGraph, \
        _populateProvenanceGraph, _populateKnowledgeProvGraph, _populatePubInfoGraph, _insertEvidence, \
        _insertConsistencyCondition, _insertSufficiencyCondition

    from .utils import process_gcs
