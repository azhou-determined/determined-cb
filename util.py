import tarfile

from pathlib import Path
import xml.etree.ElementTree as xml
from typing import List
from common import Status
import tempfile


def extract_archive(filepath: Path, target_directory=None) -> Path:
    """
    Extracts a tarfile archive from specified path and outputs to
    target directory (defaults to parent of tarfile path)
    :return: output directory path of unarchived files
    """

    if not target_directory:
        target_directory = filepath.parent
    with tarfile.open(filepath, mode="r:gz") as tar_archive:
        tar_archive.extractall(path=target_directory)
        return target_directory


def find_xml_files(root_directory: Path) -> List[Path]:
    """
    Fetches all relevant junit test reports from directory. Currently no
    meaningful structure is defined. All XML child files are assumed to be
    junit test result output files.
    :return: list of XML filepaths
    """
    return list(root_directory.rglob("*.xml"))


def parse_junit_report(filepath: Path) -> List[xml.Element]:
    """
    Parses a JUnit-structured test report file into test cases.
    Expects a root node of <testsuites> containing <testcase> children.
    """
    xmltree = xml.parse(filepath)
    testsuites = xmltree.getroot()
    return testsuites.findall("testsuite/testcase")


def get_testcase_status(testcase: xml.Element) -> Status:
    """
    JUnit does not provide an explicit status result for each
    testcase report. Statuses must be inferred through presence/absence
    of testcase tags.
    """
    failure = testcase.findall("failure") or testcase.findall("error")
    skipped = testcase.findall("skipped")
    if failure:
        return Status.FAIL
    if skipped:
        return Status.SKIPPED

    return Status.SUCCESS
