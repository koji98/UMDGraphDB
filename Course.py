import requests

class DepartmentDriver:
    def __init__(self, session):
        self._session = session

    def __create_course(self, course_id, semester ):
        query = """
                MERGE (:Course {id: $id, name: $name})
                """
        
        result = self._session.run(query, parameters = {
            "id": course_id,
            "name": department_name
        })

        for record in result:
            print(record)

        return result

    def create_constraints(self):
        query = """
                CREATE CONSTRAINT ON (c:Course)
                ASSERT c.id IS UNIQUE
                """

        self._session.run(query, parameters = {})

    def fetch_and_create(self):
        res = requests.get("https://api.umd.io/v1/courses/departments")

        if (res.status_code == requests.codes.ok):
            data = res.json()

            for department in data:
                self.__create_department(department["dept_id"], department["department"])

