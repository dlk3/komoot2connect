#  Copyright (C) 2022  David King <dave@daveking.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

#  Original source at https://github.com/ThePBone/KomootGPX
#  Created by ThePBone - Tim Schneeberger

import base64
import requests
import logging

class BasicAuthToken(requests.auth.AuthBase):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __call__(self, r):
        authstr = 'Basic ' + base64.b64encode(bytes(self.key + ":" + self.value, 'utf-8')).decode('utf-8')
        r.headers['Authorization'] = authstr
        return r


class KomootApi:
    def __init__(self):
        self.user_id = ''
        self.token = ''

    def __build_header(self):
        if self.user_id != '' and self.token != '':
            return {
                "Authorization": "Basic {0}".format(
                    base64.b64encode(bytes(self.user_id + ":" + self.token, 'utf-8')).decode())}
        return {}

    @staticmethod
    def __send_request(url, auth, critical=True):
        r = requests.get(url, auth=auth)
        if r.status_code != 200:
            logging.error("Error " + str(r.status_code) + ": " + str(r.json()))
            if critical:
                exit(1)
        return r

    def login(self, email, password):
        logging.debug("Logging in...")

        r = self.__send_request("https://api.komoot.de/v006/account/email/" + email + "/",
                                BasicAuthToken(email, password))

        self.user_id = r.json()['username']
        self.token = r.json()['password']

        logging.debug("Logged in as '" + r.json()['user']['displayname'] + "'")

    def get_tours(self, silent=False):
        if not silent:
            logging.debug("Fetching tours of user '" + self.user_id + "'...")

        r = self.__send_request("https://api.komoot.de/v007/users/" + self.user_id + "/tours/",
                                BasicAuthToken(self.user_id, self.token))

        return r.json()['_embedded']['tours']

    def fetch_tour(self, tour_id):
        logging.debug("Fetching tour '" + tour_id + "'...")

        r = self.__send_request("https://api.komoot.de/v007/tours/" + tour_id + ".gpx", 
                                BasicAuthToken(self.user_id, self.token))
        return r.text
