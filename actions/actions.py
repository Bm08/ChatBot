# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3


def writeTofile(data, filename):
     with open(filename, 'wb') as file:
        file.write(data)
     return[("Stored blob data into: ", filename, "\n")]

def readBlobData(filename):
    try:
        sqliteConnection = sqlite3.connect('chatbotDB.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from files where filename = ?"""
        cursor.execute(sql_fetch_blob_query, (filename,))
        record = cursor.fetchall()
        for row in record:
            print("filename = ", row[0])
            documentFile = row[1]

            print("Storing document on disk \n")
            documentPath = "C:\\Users\\lenovo\\chatbot\\sqlitedocuments\\" + filename + "_document.txt"
        
            writeTofile(documentFile, documentPath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

class QueryResourceType(Action):

    def name(self) -> Text:
        return "query_resource_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

           # conn = create_connection("../db/chabotDB.db")

            fname = tracker.get_slot("resource_type")

            get_query_results = readBlobData(fname)
            dispatcher.utter_message(text=get_query_results)

            return []
    
    