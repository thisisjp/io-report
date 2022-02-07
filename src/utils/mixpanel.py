import os
import requests


def mp_extract(path):
	resources = path.split("/")

	def extract(item):
		for r in resources:
			item = item[r]
		return item

	return extract


def default_extractor(series):
	first_key = list(series.keys())[0]
	return series[first_key]["all"]


class MixpanelDataRetriever:
	project_id = 2460815
	# see https://eu.mixpanel.com/report/2460815/settings/#project/2460815/serviceaccounts
	mixpanel_token = os.getenv('MIXPANEL_SERVICE_TOKEN', None)
	assert mixpanel_token is not None

	url = f"https://eu.mixpanel.com/api/2.0/insights?project_id={project_id}"
	headers = {
		"Accept": "application/json",
		"Authorization": f"Basic {mixpanel_token}"
	}

	@staticmethod
	def load_mixpanel_report(mixpanel_report):
		try:
			response = requests.request("GET", MixpanelDataRetriever.url + f"&bookmark_id={mixpanel_report.report_id}",
										headers=MixpanelDataRetriever.headers)
			data = response.json()
			series = data["series"]
			value = mixpanel_report.data_extractor(series)
			return value
		except:  # todo handle timeout & retries
			import traceback
			traceback.print_exc()
			return None
