
# Introducing Knowledge Provenance for Nanopublications

This repository contains the source code for creating nanopublications (nanopubs) with Knowledge Provenance information and the code for serializing nanopubs representing CORE-KB's GCS facts.

## Repository Structure
The repository is organized as follows.
- `data/` contains useful resources to create the nanopubs and all the results produced by the code: the program's log files and the serialized nanopubs. 
- `py/` contains the source code we developed to serialize nanopubs iwth knowledge provenance information and the code to serialize CORE-KB's GCS facts.
- `properties/`: contains the properties file, which comprises wome useful paths and namespaces used within the code.

### Source Code
The code divides into:
- `py/extended_nanopub`: contains the source code required to build extended nanopubs.
- `py/CoreNanopub`: contains the source code required to build the nanopubs starting from GCS facts stored in CORE-KB.
- `py/CommonNanopub`: contains the CoreNanopub's superclass with general methods used to build the nanopubs represting GCS facts stored in CORE-KB.