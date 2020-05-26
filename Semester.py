import requests

class SemesterDriver:
    def __init__(self, session):
        self._session = session

    def __semester_to_string(self, semester):
        season_number = str(semester)[4:]
        year = str(semester)[:4]
        season = ""

        if (season_number == "01"):
            season = "Spring"
        elif (season_number == "05"):
            season = "Summer"
        elif (season_number == "08"):
            season = "Fall"
        elif (season_number == "12"):
            season = "Winter"

        return season + " " + year

    def __create_semester(self, semester_id, semester_name):
        query = """
                MERGE (:Semester {id: $id, name: $name})
                """
        
        result = self._session.run(query, parameters = {
            "id": semester_id,
            "name": semester_name
        })

        for record in result:
            print(record)

        return result

    def create_constraints(self):
        query = """
                CREATE CONSTRAINT ON (s:Semester)
                ASSERT s.id IS UNIQUE
                """

        self._session.run(query, parameters = {})

    def fetch_and_create(self):
        res = requests.get("https://api.umd.io/v1/courses/semesters")

        if (res.status_code == requests.codes.ok):
            data = res.json()

            for semester in data:
                semester_name = self.__semester_to_string(semester)
                self.__create_semester(semester, semester_name)

