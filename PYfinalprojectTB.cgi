#!/usr/bin/env python3

import cgi
import mysql.connector
import jinja2

# Parse CGI input
form = cgi.FieldStorage()
gene_name = form.getvalue('gene_name')

# Set up Jinja2 environment
template_loader = jinja2.FileSystemLoader(searchpath="/var/www/html/mmontal4/practical_project")
env = jinja2.Environment(loader=template_loader)
template = env.get_template('templateTB.html')

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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Database Error</title>
    </head>
    <body>
        <h1>Error Connecting to Database</h1>
        <p>{err}</p>

        <a href="/mmontal4/practical_project/HTMLfinalprojectTB.html">Search again</a>
    </body>
    </html>
    """)
    exit()

# Prepare data for the template
exp_entries = []
pred_entries = []

query = """
SELECT * FROM {} WHERE gene_name LIKE %s;
"""

try:
    curs = conn.cursor()
    search_pattern = f'%{gene_name}%' if gene_name else ("%" + gene_name + "%")

    # Search in EXP_tuberculosis
    curs.execute(query.format("EXP_tuberculosis"), (search_pattern,))
    for row in curs.fetchall():
        exp_entries.append(dict(zip([col[0] for col in curs.description], row)))

    # Search in PRED_tuberculosis
    curs.execute(query.format("PRED_tuberculosis"), (search_pattern,))
    for row in curs.fetchall():
        pred_entries.append(dict(zip([col[0] for col in curs.description], row)))


    if not exp_entries and not pred_entries:
        # No results found, display query details
        print("Content-Type: text/html\n\n")
        print(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>No Results</title>
        </head>
        <body>
            <h1>No Results Found</h1>
            <p>Searched using the following query:</p>
            <p>With parameter: {search_pattern}</p>
            <a href="/mmontal4/practical_project/HTMLfinalprojectTB.html">Search again</a>
        </body>
        </html>
        """)
        exit()



except mysql.connector.Error as err:
    print("Content-Type: text/html\n\n")
    print(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Query Error</title>
    </head>
    <body>
        <h1>Error Running Query</h1>
        <p>{err}</p>
        <h2>Error Running Query</h2>
        <p>{search_pattern}</p>
        <a href="/mmontal4/practical_project/HTMLfinalprojectTB.html">Search again</a>
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
    gene_name=gene_name,
    exp_results=exp_entries,
    pred_results=pred_entries,
))



