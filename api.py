#!/usr/bin/python3
# coding: utf-8
from htb_class.scrapper import scrapper
from flask import Flask, redirect, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def home():
    """
    Root page
    @return: Creator and creator Team
    @rtype: json
    """
    presentation = {
    					"Creator": {
    						"Created by": "Magnussen",
    						"Root-Me Profile": "https://www.root-me.org/Magnussen",
    						"Hack The Box Profile": "https://www.hackthebox.eu/profile/126629",
    						"Personal Website": "https://www.magnussen.funcmylife.fr",
    						"Github Profile": "https://github.com/magnussen7",
    						"Gitlab Profile": "https://gitlab.com/magnussen7",
    						"Twitter Profile": "https://twitter.com/_magnussen_"
    					},
    					"Team": {
    						"Team": "funcMyLife()",
    						"Team Website": "https://www.funcmylife.fr",
    						"Github Profile": "https://github.com/funcMyLife",
    						"Gitlab Profile": "https://gitlab.com/funcmylife"
    					}
    				}

    return jsonify(presentation)

@app.route('/<id>', methods=['GET'])
def info_profile(id):
    """
    User info
    @param id: Get info for this id
    @type value: int
    @return: User's info (username, picture, points, owned system, owned user, respect, rank, challenges, recent activity, respected_by)
    @rtype: json
    """
    htb = scrapper(id)
    return jsonify(htb.parse())

@app.route('/team/<id>', methods=['GET'])
def info_team(id):
    """
    Team info
    @param id: Get info for this team id
    @type value: int
    @return: Team's info (username, picture, points, owned system, owned user, respect, rank, challenges, respected_by)
    @rtype: json
    """
    htb = scrapper(id, "https://www.hackthebox.eu/teams/profile/{0}")
    return jsonify(htb.parse(True))


if __name__ == "__main__":
	app.run(host='127.0.0.1', port='7777', threaded=True)
