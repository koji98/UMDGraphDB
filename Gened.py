import requests
import json

class GenedDriver:
    def __init__(self, session):
        self._session = session

    def __create_gened(self, gened_category, gened_id, gened_name):
        query = """
                MERGE (:Gened {category: $category, id: $id, name: $name})
                """
        
        result = self._session.run(query, parameters = {
            "category": gened_category,
            "id": gened_id,
            "name": gened_name
        })

        for record in result:
            print(record)

        return result

    def create_constraints(self):
        query = """
                CREATE CONSTRAINT ON (g:Gened)
                ASSERT g.id IS UNIQUE
                """

        self._session.run(query, parameters = {})

    def fetch_and_create(self):
        f = open("Geneds.json")
        geneds = json.load(f)

        for gened in geneds["data"]:
            self.__create_gened(gened["category"], gened["id"], gened["name"])

        f.close()