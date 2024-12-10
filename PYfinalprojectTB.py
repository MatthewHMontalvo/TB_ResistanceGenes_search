#!/usr/bin/env python3

import mysql.connector
import cgi
import cgitb

# Enable CGI traceback
cgitb.enable()

# Function to search for a gene name in the database
def search_gene_by_name(gene_name, table, connection):
    try:
        cursor = connection.cursor()

        # Add wildcards for partial matches
        search_pattern = f"%{gene_name}%"
        gene_name = search_pattern

        # Add query with placeholder for safety
        query = f"SELECT * FROM {table} WHERE gene_name LIKE %s"
        
        cursor.execute(query, (gene_name,))

        # Retrieve column names and query results
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        return columns, rows
    

    except Exception as e:
        return None, f"Error querying {table}: {e}"


# Function to generate an HTML table from the results
def html_table(columns, rows):
    html = '<table border="1" cellpadding="5" cellspacing="0">'
    html += '<tr>' + ''.join(f"<th>{col}</th>" for col in columns) + '</tr>'
    for row in rows:
        html += '<tr>' + ''.join(f"<td>{cell}</td>" for cell in row) + '</tr>'
    html += '</table>'
    return html






def main():
    # Parse user input
    form = cgi.FieldStorage()
    gene_name = form.getvalue("gene_name")


    # Output HTML header
    print("Content-type: text/html\n")

    print("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tuberculosis Resistance Gene Finder Results</title>
    </head>
          
    </body>
        <h1>Tuberculosis Resistance Gene Finder Results</h1>
          """)

    print("""

    """)

    if not gene_name:
        print("<p>No gene name provided. Please enter a gene name to search.</p>")
    else:
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                user='mmontal4',
                password='P@ssw0rd',
                host='localhost',
                database='mmontal4'
            )
        except mysql.connector.Error as err:
            print(f"<p>Failed to connect to database: {err}</p>")
            print("</body></html>")
            return

        try:
            # Search for the gene in the EXP_tuberculosis table
            columns_exp, rows_exp = search_gene_by_name(gene_name, "EXP_tuberculosis", conn)
            if rows_exp:
                print("<h2>Matches in Experimentally Confirmed TB Resistance Genes</h2>")
                print(html_table(columns_exp, rows_exp))
            else:
                print("<p>No matches found in Experimentally Confirmed TB Resistance Genes.</p>")

            # Search for the gene in the PRED_tuberculosis table
            columns_pred, rows_pred = search_gene_by_name(gene_name, "PRED_tuberculosis", conn)
            if rows_pred:
                print("<h2>Matches in Predicted TB Resistance Genes</h2>")
                print(html_table(columns_pred, rows_pred))
            else:
                print("<p>No matches found in Predicted TB Resistance Genes.</p>")

        except Exception as e:
            print("<h2>Error</h2>")
            print(f"<p>{e}</p>")
        finally:
            conn.close()

    # Second search option
    print("""
    <br><a href="/mmontal4/practical_project/HTMLfinalprojectTB.html>Search again</a>
    </body>      
    </html>
    """)


if __name__ == "__main__":
    main()
