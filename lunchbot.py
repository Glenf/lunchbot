#!/usr/bin/env python3
# encoding: utf-8
"""
Check what's for lunch at local restaurants and post to Hipchat

Prerequisites for posting to Hipchat:

Get a Hipchat token and save it in LUNCHBOT_TOKEN the environment variable
"""
from __future__ import print_function, unicode_literals

import argparse
import datetime
import os
import random
import requests

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LUNCHBOT_TOKEN = os.environ.get("LUNCHBOT_TOKEN")
LUNCHBOT_TARGET = os.environ.get("LUNCHBOT_TARGET")
LUNCHBOT_HOST = os.environ.get("LUNCHBOT_HOST")

NOW = datetime.datetime.now()

ELEKTRA_JSON = (
    "http://www.sodexo.fi/ruokalistat/output/daily_json/49/"
    + str(NOW.strftime("%y/%m/%d")) + "/fi"
)
GALAXI_JSON = (
    "http://www.sodexo.fi/ruokalistat/output/daily_json/16/"
    + str(NOW.strftime("%y/%m/%d")) + "/fi"
)
SMART_JSON = (
    "http://www.amica.fi/modules/json/json/Index?costNumber=3498&language=fi"
)

RESTAURANTS = ["elektra", "smarthouse", "galaxi"]

EMOJI = [
    "(candycorn)",
    "(basket)",
    "(cake)",
    "(cookie)",
]


def clean_smart(x):
    c = x.split('(')
    return c[0]


def lunch_smarthouse():
    """
    Get lunch from Smarthouse
    """
    response = requests.get(SMART_JSON)
    data = response.json()

    courses = []
    for day in data['MenusForDays']:
        d = day['Date'].split('-')
        d1 = d[2].split('T')
        menudate = datetime.date(int(d[0]), int(d[1]), int(d1[0]))
        now = NOW.strftime("%Y-%m-%d")
        if str(menudate) == str(now):
            for course in day['SetMenus']:
                if course['Name'] is not None:
                    courses.append(
                        '<b>' + course['Name'] + '</b>\n'
                    )

                courses.append(
                    ", ".join(map(clean_smart, course['Components']))
                )

    todays_menu = [
        "<b>Smarthouse</b> -- <a href='{0}'>{0}</a>"
        .format(data['RestaurantUrl']),
    ]

    todays_menu.extend(courses)
    return "\n<br>".join(todays_menu)


def get_sodexo(json_feed):
    """
    Get lunch from Sodexo
    """
    #  response = requests.get(ELEKTRA_JSON)
    response = requests.get(json_feed)
    data = response.json()

    courses = []

    for course in data['courses']:
        courses.append(course['title_fi'])

    todays_menu = [
        "<b>{1}</b> -- <a href='{0}'>{0}</a>"
        .format(data['meta']['ref_url'], data['meta']['ref_title']),
    ]

    todays_menu.extend(courses)
    return "<br>".join(todays_menu)


def lunch_elektra():
    """
    Get lunch from Sodexo Elektra
    """
    return get_sodexo(ELEKTRA_JSON)


def lunch_galaxi():
    """
    Get lunch from Sodexo Galaxi
    """
    return get_sodexo(GALAXI_JSON)


def main():
    parser = argparse.ArgumentParser(
        description="Post what's for lunch at local restaurants to HipChat",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-r", "--room",
        help="Send to this Hipchat room number instead of default one")
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="Don't post to Hipchat")
    parser.add_argument(
        "-o", '--host',
        help="Location of your self hosted hipchat")
    parser.add_argument(
        "-t", '--token',
        help="HipChat token")
    args = parser.parse_args()

    random.shuffle(RESTAURANTS)

    for restaurant in RESTAURANTS:

        if restaurant == "elektra":
            menu = lunch_elektra()
        elif restaurant == "smarthouse":
            menu = lunch_smarthouse()
        elif restaurant == "galaxi":
            menu = lunch_galaxi()

        if args.room:
            target = "{}".format(args.room)
        else:
            target = LUNCHBOT_TARGET

        if args.host:
            host = "{}".format(args.host)
        else:
            host = LUNCHBOT_HOST

        if args.token:
            token = "{}".format(args.token)
        else:
            token = LUNCHBOT_TOKEN

        hipchat_opts = {
            "color": "green",
            "notify": "true",
            "message_format": "html",
            "message": menu
        }

        hipchat_url = (
            "https://{}/v2/room/{}/notification?auth_token={}"
            ).format(host, target, token)

        hipchat_cmd = (
            "curl -d {} -H 'Content-Type: application/json' {} "
            ).format(hipchat_opts, hipchat_url)

        if args.dry_run:
            print("\n\n" + hipchat_cmd + "\n\n")
            print(menu)

        if not args.dry_run:

            response = requests.post(hipchat_url, json=hipchat_opts)


if __name__ == "__main__":
    main()

# End of file
