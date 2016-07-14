
using the JGI database for metagenomic analysis

python download-files.py 
  - asks for JGI login user and password 
  - downloads metagenomic projects from JGI database into directory ../files/
  - copies all fasta files into directory ../fasta/ 
  - copies all metadata files into directory ../config/ 

writes names of projects that couldn't be downloaded to the the following text files found in directory ../files/ 
  - nopermiss_files.txt : XML download page could not be parsed
  - unfound_files.txt : no files found to download 
  - nofasta_files.txt : files were downloaded but couldn't find fasta file
  - noconfig_files.txt : files were downloaded but couldn't find metadata
