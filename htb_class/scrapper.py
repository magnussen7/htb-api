#!/usr/bin/python3
# coding: utf-8
import argparse
import requests
import re
from bs4 import BeautifulSoup

class scrapper(object):
    def __init__(self, profile_id, base_url="https://www.hackthebox.eu/profile/{0}"):
        self.set_profile_url(base_url, profile_id)
        self.set_request()
        self.__regex_activity = "(?P<username>.*)\sowned\s(?P<type>(challenge|user|root))\s\s(?P<name>.*)\s\[\+(?P<points>\d*)\s]"
        self.__regex_time = "(?P<value>\d*)\s(?P<unit>\w*)\sago"

    def set_profile_url(self, base_url, profile_id):
        self.__profile_url = base_url.format(profile_id)

    def get_profile_url(self):
        return self.__profile_url

    def set_request(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}
        self.__request = requests.get(self.get_profile_url(), headers=headers,  allow_redirects=False)

    def get_request(self):
        return self.__request

    def __get_main_container(self):
        request = self.get_request()
        soup = BeautifulSoup(request.text, 'html.parser')
        container = soup.findAll('div', {'class': 'container'})
        return container[1]

    def __parse_info_overview(self, container):
        info_overview = container.findAll('div', {'class': 'row mb-5'})[0]
        profile_picture = info_overview.find('img')['src']
        username = info_overview.find('h2').text.capitalize()
        points = int(info_overview.find('span', {'title': 'Points'}).text.strip())
        owned_systems = int(info_overview.find('span', {'title': 'Owned Systems'}).text.strip())
        owned_users = int(info_overview.find('span', {'title': 'Owned Users'}).text.strip())
        respect = int(info_overview.find('span', {'title': 'Respect'}).text.strip())
        rank = info_overview.find('span', {'title': 'Rank'}).text.strip().capitalize()
        return {
                    'username': username,
                    'profile_picture': profile_picture,
                    'points': points,
                    'owned_systems': owned_systems,
                    'owned_users': owned_users,
                    'respect': respect,
                    'rank_name': rank
        }

    def __parse_ranking(self, container):
        ranking = container.findAll('div', {'class': 'col-sm-12 col-md-6 my-5'})[0]
        row_ranking = ranking.findAll('tr', {'class': 'table-highlight'})[0]
        cell_rank = row_ranking.findAll('td')
        rank = int(cell_rank[0].text.strip())
        challenges = int(cell_rank[-1].text.strip())
        return {
            'rank': rank,
            'total_challenges': challenges
        }

    def __parse_challenges(self, container):
        challenges = container.findAll('div', {'class': 'col-sm-12 col-md-6 my-5'})[1]
        row_challenges = challenges.findAll('tr')
        del row_challenges[0]
        challenges_score = []

        for row in row_challenges:
            cells = row.findAll('td')
            challenges_score.append({'category': cells[0].text.strip().capitalize(), 'percent': cells[1].text.strip()})

        return {
            'challenges': challenges_score
        }

    def __parse_respect(self, container):
        respect = container.findAll('div', {'class': 'col-sm-12 col-md-6 my-5'})[2]
        div_respect = respect.findAll('div', {'class': 'col-md-4'})
        user_respect = []

        for user in div_respect:
            user_respect.append({'username': user.text.strip(), 'profile_picture': user.find('img')['src']})

        return {
            'respected_by': user_respect
        }


    def __parse_recent_activity(self, container):
        recent_activity = container.findAll('div', {'class': 'col-sm-12 col-md-6 my-5'})[5]
        div_recent_activity = recent_activity.findAll('div', {'class': 'my-4 user-activity'})
        activities = []

        for activity in div_recent_activity:
            activity_match = re.match(self.__regex_activity, activity.find('p').text)
            time_match = re.match(self.__regex_time, activity.find('small').text)

            if activity_match is not None and time_match is not None:
                activities.append({
                    'name': activity_match.group('name'),
                    'type': activity_match.group('type'),
                    'points': activity_match.group('points'),
                    'time_value': time_match.group('value'),
                    'time_unit': time_match.group('unit')
                })

        return {
            'recent_activity': activities
        }

    def parse(self):
        result = {}
        print(self.get_request().status_code)
        if self.get_request().status_code == requests.codes.ok:
            container = self.__get_main_container()
            info_overview = self.__parse_info_overview(container)
            ranking = self.__parse_ranking(container)
            challenges = self.__parse_challenges(container)
            respect = self.__parse_respect(container)
            recent_activity = self.__parse_recent_activity(container)

            result.update(info_overview)
            result.update(ranking)
            result.update(challenges)
            result.update(recent_activity)
            result.update(respect)
            return result
        else:
            return {
                'owned_systems': '',
                'respected_by': [],
                'rank': '',
                'points': 0,
                'profile_picture': '',
                'username': '',
                'total_challenges': 0,
                'challenges': [],
                'recent_activity': [],
                'rank_name': '',
                'owned_users': 0,
                'respect': 0
            }
