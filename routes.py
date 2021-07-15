from flask import request, Response, abort
import services
import logging
from threading import Thread
import tempfile
from pathlib import Path
from app import app
from functools import wraps


def require_access_key(f):
	"""
	Flask route function decorator that authenticates requests. Only allows requests
	with a valid API key header (currently only one token).

	:param f: flask function
	:return: function if successful, else abort
	"""

	@wraps(f)
	def decorated_function(*args, **kwargs):
		if validate_api_key(request.headers.get("x-api-key")):
			return f(*args, **kwargs)
		else:
			logging.error(f"Invalid access key from {request.remote_addr}")
			abort(401)
	return decorated_function


def validate_api_key(api_key):
	if not api_key:
		logging.error("API key not specified")
		return False

	if app.config["APP_ACCESS_KEY"] and app.config["APP_ACCESS_KEY"] == api_key:
		return True

	return False


@app.route("/upload", methods=["POST"])
@require_access_key
def upload():
	"""
	Route requires Determined access token.

	Handles upload of XML-structured test result data files
	for a single test suite run, currently defined as a CircleCi "job".

	Expects an archived file containing junit-like test reports and a
	CircleCi build ID. Multiple reports will be treated as result data for
	the singular given build ID.
	"""

	files = request.files.to_dict()
	job_id = request.form["job_id"]
	if not files or not job_id:
		logging.error("Cannot upload test results. Job ID and files must be specified.")
		return Response(response="Invalid input parameters", status=422)

	test_report = files["report"]

	# Save the archive in a temporary location for asynchronous processing and return to client
	archive_filepath = Path(tempfile.mkdtemp()) / f"{job_id}-test_results.tar.gz"
	test_report.save(archive_filepath)

	thread = Thread(target=services.process_upload, args=(job_id, archive_filepath,))
	thread.start()
	return Response(response=f"Upload of {len(files)} files for job {job_id} received", status=200)

