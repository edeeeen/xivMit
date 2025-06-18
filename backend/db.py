#################################################################
#                Database Interaction Class                     #
#################################################################
import pyodbc
from fastapi import HTTPException

class db:
    def __init__(self, cnxn_object):
        # Store the pyodbc connection object
        self.cnxn = cnxn_object
        print("DB handler initialized with provided connection.")

    # Unimplemented
    # Queries DB for templates under the input encounter
    def getTemplates(self, encounter):
        return {}
    
    def getEncounters(self):
        # Check if db connection is good
        if not self.cnxn:
            print("ERROR: No database connection found in getEncounters.")
            # Raise execption
            raise HTTPException(status_code=500, detail="Database connection not active.")
        
        # Query all of dbo.Encounters
        query = "SELECT tier, shorthand, boss, imgLink FROM dbo.Encounters"

        try:
            # Make cursor and execute query
            cursor = self.cnxn.cursor()
            cursor.execute(query)
            
            # Fetch column names from cursor description
            columns = [column[0] for column in cursor.description]
            
            rows = cursor.fetchall()
            cursor.close()
            
            # Convert each row to a dictionary
            results_as_dicts = []
            for row in rows:
                row_dict = {}
                for i, col_name in enumerate(columns):
                    row_dict[col_name] = row[i]
                results_as_dicts.append(row_dict)
            
            print(f"Encounters fetched successfully. Count: {len(results_as_dicts)}")
            return results_as_dicts # Return list of dictionaries
            
        except pyodbc.Error as e:
            print(f"Error fetching encounters: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred in getEncounters: {e}")
            raise
