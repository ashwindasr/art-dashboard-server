"""
This module has helper functions to make http requests to other apis.
"""

import requests
import ocp_build_data.constants as app_constants
import lib.constants as constants
import traceback
import os
import yaml
import time


def get_all_ocp_build_data_branches():

    """
    This function lists all the branches of the ocp-build-data repository.
    :return: dict, all the branches along with their details.
    """

    access_token = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

    try:
        req = requests.get(app_constants.GITHUB_URL_TO_LIST_ALL_OCP_BUILD_DATA_BRANCHES,
                           headers={"Authorization": "token " + access_token})
        branches = req.json()
        branches_data = []

        for branch in branches:
            if "name" in branch:
                if constants.OCP_BUILD_DATA_RELEVANT_BRANCHES_REGEX_COMPILER.match(branch["name"]):
                    branch_data = dict()
                    branch_data["name"] = branch["name"]
                    version = branch["name"].split("openshift-")[1]
                    branch_data["version"] = version
                    branch_data["priority"] = 0
                    branch_data["extra_details"] = branch
                    branches_data.append(branch_data)
        branches_data = sorted(branches_data, key=lambda k: k["version"], reverse=True)
        return branches_data

    except Exception as e:
        traceback.print_exc()
        return []


def get_branch_details_for_ocp_build_data(branch_name):

    branch_group_yml_url = get_group_yml_file_url(branch_name)
    return branch_group_yml_url


def get_group_yml_file_url(branch_name: str) -> dict:

    """
    This method takes a branch name of ocp_build_data as a parameter and returns advisories details for the same.
    :param branch_name: Branch name of ocp_build_data
    :return: adivsories details
    """
    access_token = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
    hit_url = app_constants.GITHUB_GROUP_YML_CONTENTS_URL.format(branch_name)
    hit_request = requests.get(hit_url, headers={"Authorization": "token " + access_token})
    return hit_request.json()["download_url"]


def get_github_rate_limit_status():
    access_token = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
    hit_request = requests.get(os.environ["GITHUB_RATELIMIT_ENDPOINT"], headers={"Authorization": "token " + access_token})
    hit_response = hit_request.json()
    hit_response = hit_response["rate"]
    hit_response["reset_secs"] = hit_response["reset"] - time.time()
    hit_response["reset_mins"] = int((hit_response["reset"] - time.time())/60)
    return hit_response


def get_branch_advisory_ids(branch_name):
    group_yml_url = os.environ["GITHUB_RAW_CONTENT_URL"].format(branch_name)
    access_token = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
    hit_request = requests.get(group_yml_url,
                               headers={"Authorization": "token " + access_token})
    hit_response = yaml.load(hit_request.text)
    if "advisories" in hit_response:
        return hit_response["advisories"]
    return {}
