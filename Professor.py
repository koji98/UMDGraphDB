import requests
from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
    "bolt://52.3.248.178:34364", 
    auth=basic_auth("neo4j", "tour-consequences-towns"))
session = driver.session()

grabMoreProfessors = True
pageNumber = 1

# while (grabMoreProfessors):
#     res = requests.get("https://api.umd.io/v1/professors?page=" + str(pageNumber))

#     if(not(res)):
#         grabMoreProfessors = False
#     else:
#         data = res.json()
#         pageNumber = pageNumber + 1
#         for professor in data:
#             createProfessorCypher = """
#                                     CREATE (p: Professor) 
#                                     SET p.Name = \"{}\"
#                                     """.format(professor["name"])

#             # print(createProfessorCypher)

#             results = session.run(createProfessorCypher, parameters={})

#             for record in results:
#                 print(record)

#             matchProfessorCypher = """
#                                    MATCH (prof: Professor {{Name: \"{}\"}}) 
#                                    RETURN prof.Name
#                                    """.format(professor["name"])

#             # print(matchProfessorCypher)

#             results = session.run(matchProfessorCypher, parameters={})

#             for record in results:
#                 print(record)

#             for course in professor["taught"]:
#                 createCourseCypher = """
#                                      CREATE (c: Course)
#                                      SET c.Course_Id = \"{}\", c.Semester = \"{}\"
#                                      """.format(course["course_id"], course["semester"])

#                 # print(createCourseCypher)

#                 results = session.run(createCourseCypher, parameters={})

#                 for record in results:
#                     print(record)

#                 matchCourseCypher = """
#                                     MATCH (course: Course {{Course_Id: \"{}\"}})
#                                     RETURN course.Course_Id
#                                     """.format(course["course_id"])

#                 # print(matchCourseCypher)

#                 results = session.run(matchCourseCypher, parameters={})

#                 for record in results:
#                     print(record)

#                 mergeProfessorCourseCypher = """
#                                              MATCH (a:Professor), (b:Course)
#                                              WHERE a.Name = \"{}\" AND b.Course_Id = \"{}\" AND b.Semester = \"{}\"
#                                              CREATE (a)-[r:TAUGHT]->(b)
#                                              RETURN r
#                                              """.format(professor["name"], course["course_id"], course["semester"])

#                 print(mergeProfessorCourseCypher)

#                 results = session.run(mergeProfessorCourseCypher, parameters={})

#                 for record in results:
#                     print(record)
            
        