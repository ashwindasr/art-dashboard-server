
import os
import requests
import time
from typing import Optional
from slack_sdk import WebClient

slack_token = os.environ.get('SLACK_TOKEN', None)
def post_slack_message(message: str, thread_ts: Optional[str] = None, channel: Optional[str] = "#forum-ocp-release"):
    return WebClient(token=slack_token).chat_postMessage(channel=channel, text=message, thread_ts=thread_ts, username="art-release-bot", link_names=True, attachments=[], icon_emoji=":dancing_robot:", reply_broadcast=False)


# check release need to prepare
releases_needs_prepare = requests.get("https://art-dash-server-hackspace-ximhan.apps.artc2023.pc3z.p1.openshiftapps.com/api/v1/release_prepare_alert").json()
if releases_needs_prepare['releases'] != []:
    release_msg = "\n".join(f"• {msg[0]} : {msg[1]}, latest <https://amd64.ocp.releases.ci.openshift.org/releasestream/{msg[2]}.0-0.nightly/release/{msg[3]}|{msg[3]}> is {msg[4]}" for msg in releases_needs_prepare['releases'])
    post_slack_message(f"We need to prepare the following releases today:\n{release_msg}", thread_ts=None, channel="#team-art")


# check and monitor release advisory status
release_status = requests.get("https://art-dash-server-hackspace-ximhan.apps.artc2023.pc3z.p1.openshiftapps.com/api/v1/release_status").json()
if release_status['alert'] != []:
    response = post_slack_message(' \n'.join([msg['status'] for msg in release_status['alert']]))
    print(f"message posted in https://redhat-internal.slack.com/archives/{response['channel']}/p{response['ts'].replace('.', '')}")
    if release_status['unshipped'] != []:
        post_slack_message("start monitoring advisory not in shipped live status, interval set to 1 hour ...", thread_ts=response['ts'])
        duration = 1
        alert_artist = False
        while release_status['unshipped'] != []:
            for item in release_status['unshipped']:
                advisory_status_response = requests.get(f"https://art-dash-server-hackspace-ximhan.apps.artc2023.pc3z.p1.openshiftapps.com/api/v1/advisory_activites/?advisory={item['advisory']}").json()
                advisory_status = advisory_status_response['data'][-1]['attributes']['added'] if len(advisory_status_response['data']) > 0 else "NEW_FILES"
                if advisory_status in ["SHIPPED_LIVE", "DROPPED_NO_SHIP"]:
                    release_status['unshipped'].remove(item)
                    post_slack_message(f"{item['note']} status changed to {advisory_status}", thread_ts=response['ts'])
                    # extra advisory changed to shipped_live
                    if "extra" in item['note'] and advisory_status == "SHIPPED_LIVE":
                        if int(item['note'].split(' ')[0].split('.')[1]) < 19:
                            trigger_jenkins_response = requests.get(f"https://art-dash-server-hackspace-ximhan.apps.artc2023.pc3z.p1.openshiftapps.com/api/v1/trigger_jenkins_job/?assembly={item['note'].split(' ')[0]}").json()
                            post_slack_message(f"<{trigger_jenkins_response['build_url']}|operator_sdk> job for {item['note'].split(' ')[0]} triggered", thread_ts=response['ts'])

            print(f"sleeping 1 hours due to {release_status['unshipped']}")
            time.sleep(3600)
            duration = duration + 1
            if duration > 24 and not alert_artist:
                post_slack_message("@release-artists those advisories are not all shipped after a day of ship day, please take a look a push them ship as soon as possible", thread_ts=response['ts'])
                alert_artist = True
        post_slack_message("All advisory now in shipped live status, stop monitoring", thread_ts=response['ts'])
else:
    print("No alert", [msg['status'] for msg in release_status['message']])

