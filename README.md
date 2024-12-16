The aim of this project is to develop a user-friendly tool that allows researchers and
clinicians to quickly determine if specific genes within TB have both known and predicted
antibiotic resistance associated with them.

*ABOUT *
Web front-end for Mycobacterium tuberculosis gene and sequence search, enabling users to identify confirmed and predicted antibiotic-resistance genes.

The source code is available in the university server under the path:
/var/www/html/mmontal4/practical_project/


Access to the webpage and searches can be found with: (when accessing the university server and VPN)

http://bfx3.aap.jhu.edu/mmontal4/practical_project/HTMLfinalprojectTB.html


The application includes the following key functionalities:
1	A search interface to query a user’s gene (or genes) of interest and compare them against the BacMet Resistance Genes Database.

2	A FASTA-based search function to identify the top 5 best-matching genes, with detailed results on associated resistance genes.


*REQUIREMENTS *
	•	Dependencies: Python 3, Jinja2 for templating, MySQL for database management, Bio.Seq and Bio.Align for sequence alignment and scoring.
	•	Storage: Minimal storage is required for query inputs, but sufficient space is needed for storing genome data.


*PROGRAM USAGE *
1	Gene Search
	◦	Enter a gene name or keyword into the search box.
	◦	Click "Search" to query the database for matching gene records.
	◦	View results, including gene attributes and associated resistance genes.

2	FASTA Sequence Search
	◦	Enter a FASTA sequence in the provided input box or upload a sequence file.
	◦	Click "Submit" to find the top 5 best-matching genes.
	◦	Review results, including match scores and details of any resistance-associated genes.

3	Results
	◦	Results are shown in an HTML table with alternating row colors for ease of reading
	◦	Results are separated to indicate the experimentally confirmed and predicted matches


*DEMO DATA *
Mycobacterium tuberculosis genome and gene data are stored in the database for recall during user queries. These data are based on publicly available genomic datasets from BacMet.

Reference: BacMet Resistance Genes Database: https://bacmet.biomedicine.gu.se/


*ACKNOWLEDGEMENTS *
This project is powered by:
	•	MySQL for efficient database management.
	•	BacMet for antibiotic resistance genes and annotations.
	•	Python and Jinja2 for backend scripting and web template rendering.
	•	Bio.Align package for alignment scoring - https://biopython.org/docs/1.75/api/Bio.Align.html


*REFERENCES *
BacMet. (2018). BacMet: Antibacterial Biocide and Metal Resistance Genes Database. Biomedicine.gu.se. http://bacmet.biomedicine.gu.se/index.html





