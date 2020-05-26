import requests

class DepartmentDriver:
    def __init__(self, session):
        self._session = session

    def __create_department(self, department_id, department_name):
        query = """
                MERGE (:Department {id: $id, name: $name})
                """
        
        result = self._session.run(query, parameters = {
            "id": department_id,
            "name": department_name
        })

        for record in result:
            print(record)

        return result

    def create_constraints(self):
        query = """
                CREATE CONSTRAINT ON (d:Department)
                ASSERT d.id IS UNIQUE
                """

        self._session.run(query, parameters = {})

    def fetch_and_create(self):
        res = requests.get("https://api.umd.io/v1/courses/departments")

        if (res.status_code == requests.codes.ok):
            data = res.json()

            for department in data:
                self.__create_department(department["dept_id"], department["department"])

