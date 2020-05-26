import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, basic_auth
from Semester import SemesterDriver
from Department import DepartmentDriver
from Gened import GenedDriver

project_folder = os.path.expanduser("~/UMDGraphDB")
load_dotenv(verbose=True)

driver = GraphDatabase.driver(
    os.getenv("BOLT_URL"), 
    auth=basic_auth(os.getenv("USER"), os.getenv("PASSWORD")))
session = driver.session()

# CREATE Semester Information.
semester_driver = SemesterDriver(session)
# semester_driver.create_constraints()
# semester_driver.fetch_and_create()

# CREATE Department Information.
department_driver = DepartmentDriver(session)
# department_driver.create_constraints()
# department_driver.fetch_and_create()

# CREATE Gened Information.
gened_driver = GenedDriver(session)
# gened_driver.create_constraints()
# gened_driver.fetch_and_create()

# CREATE Course Information.


driver.close()