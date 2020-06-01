import requests
import time
from dotenv import load_dotenv
from neo4j import GraphDatabase, basic_auth
import os

class ProfessorDriver:
    def __init__(self, driver):
        self._driver = driver
        self._id = 0

    def __create_professor(self, professor):
        try:
            with self._driver.session() as session:
                for course in professor["taught"]:
                    query = """
                            MATCH x = (c:Course{id: $course_id})-[:DURING]->(s:Semester{id: $semester_id})
                            FOREACH (n IN nodes(x) | MERGE (p:Professor{id: $professor_id, name: $professor_name}), (p)-[:TAUGHT]->(n))
                            """

                    print(query)
                    
                    result = session.run(query, parameters = {
                        "course_id": course["course_id"],
                        "semester_id": course["semester"],
                        "professor_id": self._id,
                        "professor_name": professor["name"]
                    })

                self._id = self._id + 1
        except:
            print("CLOSED PROFESSOR")
            self._driver.close()
            self._driver = GraphDatabase.driver(os.getenv("BOLT_URL"), auth=basic_auth(os.getenv("USER"), os.getenv("PASSWORD")))
            self.__create_professor(professor)

    def create_constraints(self):
        try:
            with self._driver.session() as session:
                query = """
                        CREATE CONSTRAINT ON (p:Professor)
                        ASSERT p.id IS UNIQUE
                        """

                session.run(query, parameters = {})
        except:
            self._driver.close()
            self._driver = GraphDatabase.driver(os.getenv("BOLT_URL"), auth=basic_auth(os.getenv("USER"), os.getenv("PASSWORD")))
            self.create_constraints()

    def fetch_and_create(self):
        page = 1

        while(True):
            api_url = "https://api.umd.io/v1/professors?page={}".format(page)
            print(api_url)
            try:
                res = requests.get(api_url)
            except:
                print("FAILED REQUEST - " + api_url)
                sleep(120)
                print("CONTINUING")
                continue
            page = page + 1
            data = res.json()

            if (len(data) > 0):
                for professor in data:
                    self.__create_professor(professor)
            else:
                break

    def close(self):
        self._driver.close()