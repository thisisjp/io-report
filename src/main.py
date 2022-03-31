from models.io_users import IOUsersReport
from models.mixpanel import sections, users_section
from utils.slack import send_slack_message_blocks
import datetime

'''
env variable to setup
MIXPANEL_SERVICE_TOKEN: the token used to authenticate requests to the Mixpanel API
SLACK_WEB_HOOK: webhook used to send the report to Slack dedicated channel 
'''

today = datetime.datetime.now()
week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
header = f":bar_chart: <https://github.com/pagopa/io-report|IO weekly report> dal *{week_ago.day}/{week_ago.month}* al *{today.day}/{today.month}*"
slack_msgs = []

# collect reports
# io user report
io_user_report = IOUsersReport(f"utenti hanno effettuato l'accesso (dal 16/04/2020)")
# pre-pend io_user_report as first element of users_section
users_section.add_report(io_user_report, 0)

for idx, section in enumerate(sections):
	if idx > 0:
		slack_msgs.append("")  # empty line divider
	slack_msgs.append(section.header)
	for r in section.reports:
		print(f"requesting data for '{r.description}'...")
		data = r.load_data()
		if data is None:
			raise IOError(f"cannot retrieve data for report '{r.description}'")
		slack_msgs.append(f"- `{data}` {r.description}")

if len(slack_msgs):
	send_slack_message_blocks([header])
	send_slack_message_blocks(["\n".join(slack_msgs)])
