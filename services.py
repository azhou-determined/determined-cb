import dao
import api.circleci as api
import util
import xml.etree.ElementTree as xml
from common import Status
import logging
import shutil


def process_upload(job_id, report_path):
    job = save_job_details(job_id)
    reports_dir = util.extract_archive(report_path)
    test_reports = util.find_xml_files(reports_dir)
    for test_report in test_reports:
        testcases = util.parse_junit_report(test_report)
        for testcase in testcases:
            save_test_result(job.id, testcase)
    shutil.rmtree(reports_dir)


def save_job_details(job_id):
    job_details = api.get_job_details(job_id)

    return dao.create_job(name=job_details["workflows"]["job_name"],
                          status=Status(job_details["status"]).name,
                          branch=job_details["branch"],
                          user=job_details["author_email"],
                          commit=job_details["vcs_revision"],
                          start_time=job_details["start_time"],
                          end_time=job_details["stop_time"],
                          duration=job_details["build_time_millis"] * 0.001,
                          circleci_url=job_details["build_url"])


def save_test_result(job_id, testcase: xml.Element) -> None:
    """
    Reads the JUnit element of a singular test case and persists relevant
    data to the database.
    """
    name = testcase.get("name")
    classname = testcase.get("classname")
    if not name or not classname:
        logging.error(f"Unable to save test result for job {job_id}: "
                      f"missing name or classname")
        return

    dao.create_test(job_id=job_id, name=name,
                    classname=classname,
                    status=util.get_testcase_status(testcase),
                    duration=testcase.get("time"))

