# BasicDBUtils - Part of ProjRec Project

import sqlite3
from typing import Any


class Utils:
    def __init__(self, db_name):
        self.db_name = db_name

    def read_from_db(self):
        connector = sqlite3.connect(f"{self.db_name}.db")
        pointer = connector.cursor()
        pointer.execute("SELECT * FROM ProjDetails")
        project_details: list[Any] = pointer.fetchall()
        pointer.execute("SELECT * FROM ProjRec")
        proj_rec: list[Any] = pointer.fetchall()
        connector.close()
        return project_details, proj_rec

    def create_new_project(self):
        connector = sqlite3.connect(f"{self.db_name}.db")
        pointer = connector.cursor()
        try:
            pointer.execute("""CREATE TABLE IF NOT EXISTS ProjDetails (
                            [Name of Project] TEXT    NOT NULL,
                            [Team Leader]     TEXT    NOT NULL,
                            [Team Member 1]   TEXT    NOT NULL,
                            [Team Member 2]   TEXT    NOT NULL,
                            [Team Member 3]   TEXT    NOT NULL,
                            [Team Member 4]   TEXT    NOT NULL,
                            Domain            TEXT    NOT NULL,
                            Category          TEXT    NOT NULL,
                            Description       TEXT    NOT NULL,
                            [Project Link]    TEXT    NOT NULL,
                            Version           REAL    NOT NULL,
                            Status            BOOLEAN NOT NULL
                            );""")
            pointer.execute("""CREATE TABLE IF NOT EXISTS ProjRec (
                            id                   INTEGER  PRIMARY KEY
                                                          UNIQUE
                                                          NOT NULL,
                            [Work Assigned]      TEXT     NOT NULL,
                            [Assigned To]        TEXT     NOT NULL,
                            [Work Description]   TEXT     NOT NULL,
                            [Date Work Assigned] DATETIME NOT NULL,
                            Status               TEXT     NOT NULL,
                            [Date of Completion] DATETIME NOT NULL
                            );""")
            connector.commit()
        except sqlite3.OperationalError:
            pass
        finally:
            connector.close()

    def add_entry_details(self, ProjDetails_input):
        connector = sqlite3.connect(f"{self.db_name}.db")
        pointer = connector.cursor()
        pointer.execute(f"""INSERT INTO ProjDetails VALUES("{ProjDetails_input["Name"]}", 
                        "{ProjDetails_input["Team Leader"]}", 
                        "{ProjDetails_input["Team Member 1"]}", 
                        "{ProjDetails_input["Team Member 2"]}", 
                        "{ProjDetails_input["Team Member 3"]}", 
                        "{ProjDetails_input["Team Member 4"]}", 
                        "{ProjDetails_input["Domain"]}", 
                        "{ProjDetails_input["Category"]}", 
                        "{ProjDetails_input["Description"]}", 
                        "{ProjDetails_input["Project Link"]}", 
                        {ProjDetails_input["Version"]}, 
                        "{ProjDetails_input["Status"]}");""")
        connector.commit()
        connector.close()

    def add_entry_record(self, ProjectRec_input):
        connector = sqlite3.connect(f"{self.db_name}.db")
        pointer = connector.cursor()
        try:
            pointer.execute(f"""INSERT INTO ProjRec VALUES({ProjectRec_input["ID"]}, 
                            "{ProjectRec_input["Task Assigned"]}", 
                            "{ProjectRec_input["Assigned to"]}", 
                            "{ProjectRec_input["Description"]}", 
                            "{ProjectRec_input["Date Assigned"]}", 
                            "{ProjectRec_input["Status"]}", 
                            "{ProjectRec_input["Date Completed"]}");""")
            connector.commit()
        except sqlite3.IntegrityError:
            print("Add an unique id")
        finally:
            connector.close()

    def delete_record(self, id_):
        connector = sqlite3.connect(f"{self.db_name}.db")
        pointer = connector.cursor()
        pointer.execute(f'DELETE FROM ProjRec WHERE id = \'{str(id_)}\';')
        connector.commit()
        connector.close()

    def modify_record(self, id_, field, value):
        connector = sqlite3.connect(f"{self.db_name}.db")
        pointer = connector.cursor()
        pointer.execute(f'UPDATE ProjRec SET \'{str(field)}\' = \'{str(value)}\' WHERE id = \'{str(id_)}\';')
        connector.commit()
        connector.close()

    def modify_details(self, field, value):
        connector = sqlite3.connect(f"{self.db_name}.db")
        pointer = connector.cursor()
        pointer.execute(f'UPDATE ProjDetails SET \'{str(field)}\' = \'{str(value)}\';')
        connector.commit()
        connector.close()
