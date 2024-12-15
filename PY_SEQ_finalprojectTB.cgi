#!/usr/bin/env python3

import cgi
import mysql.connector
import jinja2
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner

# Parse CGI input
form = cgi.FieldStorage()
user_sequence = form.getvalue('user_sequence')

# Set up Jinja2 environment
template_loader = jinja2.FileSystemLoader(searchpath="/var/www/html/mmontal4/practical_project")
env = jinja2.Environment(loader=template_loader)
template = env.get_template('SEQ_templateTB.html')

# Initialize database connection
try:
    conn = mysql.connector.connect(
        user='mmontal4',
        password='P@ssw0rd',
        host='localhost',
        database='mmontal4'
    )
except mysql.connector.Error as err:
    print("Content-Type: text/html\n\n")
    print(f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Database Error</title>
    </head>
    <body>
        <h1>Error Connecting to Database</h1>
        <p>{err}</p>
        <a href=\"/mmontal4/practical_project/HTMLfinalprojectTB.html\">Search again</a>
    </body>
    </html>
    """)
    exit()

# Store data in appropriate variables for the template
exp_alignment_results = []
pred_alignment_results = []
exp_query = "SELECT id, gene_name, sequence FROM EXP_tuberculosis;"
pred_query = "SELECT ref_id, gene_name, sequence FROM PRED_tuberculosis;"

try:
    curs = conn.cursor(dictionary=True)

    # Fetch experimental sequences
    curs.execute(exp_query)
    exp_records = curs.fetchall()

    # Fetch predicted sequences
    curs.execute(pred_query)
    pred_records = curs.fetchall()

    if user_sequence:
        # Initialize pairwise aligner
        aligner = PairwiseAligner()
        aligner.mode = 'global'

        # Score the user sequence against experimental sequences
        exp_alignment_scores = []
        for record in exp_records:
            score = aligner.score(user_sequence, record['sequence'])
            exp_alignment_scores.append((record['id'], record['gene_name'], record['sequence'], score))

        # Sort by scores and fetch top 5 matches for experimental sequences
        exp_alignment_results = sorted(exp_alignment_scores, key=lambda x: x[3], reverse=True)[:5]

        # Score the user sequence against predicted sequences
        pred_alignment_scores = []
        for record in pred_records:
            score = aligner.score(user_sequence, record['sequence'])
            pred_alignment_scores.append((record['ref_id'], record['gene_name'], record['sequence'], score))

        # Sort by scores and fetch top 5 matches for predicted sequences
        pred_alignment_results = sorted(pred_alignment_scores, key=lambda x: x[3], reverse=True)[:5]

except mysql.connector.Error as err:
    print("Content-Type: text/html\n\n")
    print(f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Query Error</title>
    </head>
    <body>
        <h1>Error Running Query</h1>
        <p>{err}</p>
        <a href=\"/mmontal4/practical_project/HTMLfinalprojectTB.html\">Search again</a>
    </body>
    </html>
    """)
    exit()

finally:
    curs.close()
    conn.close()

# Render template with data
print("Content-Type: text/html\n\n")
print(template.render(
    user_sequence=user_sequence,
    exp_alignment_results=exp_alignment_results,
    pred_alignment_results=pred_alignment_results
))
