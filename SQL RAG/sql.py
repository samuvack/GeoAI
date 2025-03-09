import sqlite3
import json

def execute_sql_query(database_path, query, output_format="html"):
    """
    Voer een SQL-query uit op een SQLite-database en geef het resultaat terug in HTML- of JSON-indeling.
    
    Parameters:
    - database_path (str): Pad naar het SQLite-databasebestand.
    - query (str): De SQL-query om uit te voeren.
    - output_format (str): Outputindeling, 'html' of 'json'.
    
    Returns:
    - str: De resultaten in de gewenste indeling.
    """
    # Maak verbinding met de database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Voer de SQL-query uit
        cursor.execute(query)

        # Controleer of het een SELECT-query is om resultaten op te halen
        if query.strip().lower().startswith("select"):
            # Haal kolomnamen op
            column_names = [description[0] for description in cursor.description]
            results = cursor.fetchall()

            if output_format == "html":
                # HTML-tabel opbouwen
                html = "<table border='1'>"
                html += "<tr>"
                for col in column_names:
                    html += f"<th>{col}</th>"
                html += "</tr>"

                for row in results:
                    html += "<tr>"
                    for cell in row:
                        html += f"<td>{cell}</td>"
                    html += "</tr>"

                html += "</table>"
                return html

            elif output_format == "json":
                # JSON-output opbouwen
                json_data = [dict(zip(column_names, row)) for row in results]
                return json.dumps(json_data, indent=4)

            else:
                raise ValueError("Ongeldig output-formaat. Kies 'html' of 'json'.")

        else:
            # Voor andere queries (INSERT, UPDATE, DELETE), bevestig de wijzigingen
            conn.commit()
            return "Query uitgevoerd en wijzigingen doorgevoerd."
    except sqlite3.Error as e:
        return f"Fout bij het uitvoeren van de query: {e}"
    finally:
        # Sluit de verbinding
        cursor.close()
        conn.close()

# Voorbeeld van gebruik
database_path = "gebouw_gebouweenheid.db"
query = "SELECT * FROM gebouw LIMIT 10;"  # Pas aan naar je eigen query

# HTML-output
html_output = execute_sql_query(database_path, query, output_format="html")
print("HTML Output:")
print(html_output)

# JSON-output
json_output = execute_sql_query(database_path, query, output_format="json")
print("\nJSON Output:")
print(json_output)
