import requests
import time

class ProfessorDriver:
    def __init__(self, session):
        self._session = session
        self._id = 0

    def __create_professor(self, professor):
        for course in professor["taught"]:
            query = """
                    MATCH (c:Course{id: $course_id}) -[:DURING]-> (s:Semester{id: $semester_id})
                    MERGE (p:Professor{id: $professor_id, name: $professor_name}), 
                    (p) -[:TAUGHT]-> (c)
                    """
            
            result = self._session.run(query, parameters = {
                "course_id": course["course_id"],
                "semester_id": course["semester"],
                "professor_id": self._id,
                "professor_name": professor["name"]
            })

        self._id = self._id + 1

    def create_constraints(self):
        query = """
                CREATE CONSTRAINT ON (p:Professor)
                ASSERT p.id IS UNIQUE
                """

        self._session.run(query, parameters = {})

    def fetch_and_create(self):
        page = 1

        while(True):
            time.sleep(60)
            api_url = "https://api.umd.io/v1/professors?page={}".format(page)
            print(api_url)
            try:
                res = requests.get(api_url)
            except:
                print("FAILED REQUEST - " + api_url)
                sleep(600)
                print("CONTINUING")
                continue
            page = page + 1
            data = res.json()

            if (len(data) > 0):
                for professor in data:
                    self.__create_professor(professor)
            else:
                break
