import requests
import time

class CourseDriver:
    def __init__(self, session):
        self._session = session

    def __create_course(self, semester_record, course_id, semester, course_name, dept_id, credits, desc, geneds, relationships):
        query_create_rel = """
                           MATCH (s:Semester{id: $semester_id}), (d:Department{id: $department_id})
                           CREATE (c:Course{id: $course_id, name: $course_name, credits: $credits, description: $desc}),
                           (c) -[:DURING]-> (s), (c) -[:WITHIN]-> (d)
                           RETURN c, d, s
                           """

        result = self._session.run(query_create_rel, parameters = {
            "semester_id": semester,
            "department_id": dept_id,
            "course_id": course_id,
            "course_name": course_name,
            "credits": credits,
            "desc": desc
        })

        return result

    def __grab_semesters(self):
        query = """
                MATCH (s:Semester) RETURN s
                """

        return self._session.run(query, parameters = {})

    def fetch_and_create(self):
        for record in self.__grab_semesters():
            semester = record[0]["id"]
            page = 1

            while (True):
                time.sleep(60)
                api_url = "https://api.umd.io/v1/courses?semester={0}&page={1}".format(semester, page)
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
                    for course in data:
                        self.__create_course(record[0], course["course_id"], semester, course["name"], course["dept_id"], course["credits"], course["description"], course["gen_ed"], course["relationships"])
                else:
                    break

