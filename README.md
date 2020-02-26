# Hack the Box API

A python script which creates an API for public profile on https://www.hackthebox.eu

Your profile must be public (On *Hack the Box* > [Settings](https://www.hackthebox.eu/home/settings) > *Make my profile public.*)

## List of endpoints

You need to use the id from the profile url.

Example :
  https://www.hackthebox.eu/profile/126629

### API info : /

Example :

```
> curl 127.0.0.1:7777
{
  "Creator": {
    "Twitter Profile": "https://twitter.com/_magnussen_",
    "Created by": "Magnussen",
    "Personal Website": "https://www.magnussen.funcmylife.fr",
    "Github Profile": "https://github.com/magnussen7",
    "Gitlab Profile": "https://gitlab.com/magnussen7",
    "Root-Me Profile": "https://www.root-me.org/Magnussen",
    "Hack The Box Profile": "https://www.hackthebox.eu/profile/126629"
  },
  "Team": {
    "Team Website": "https://www.funcmylife.fr",
    "Github Profile": "https://github.com/funcMyLife",
    "Gitlab Profile": "https://gitlab.com/funcmylife",
    "Team": "funcMyLife()"
  }
}
```

### User info : /*id*

Example :

```
> curl 127.0.0.1:7777/126629
{
  "recent_activity": [
    {
      "time_value": "1",
      "points": "10",
      "time_unit": "week",
      "name": "Postman",
      "type": "user"
    },
    {
      "time_value": "1",
      "points": "20",
      "time_unit": "week",
      "name": "Traverxec",
      "type": "root"
    },
                .
                .
                .
  ],
  "owned_systems": 4,
  "points": 24,
  "challenges": [
    {
      "percent": "2.13%",
      "category": "Reversing"
    },
    {
      "percent": "0%",
      "category": "Crypto"
    },
               .
               .
               .
  ],
  "rank_name": "Script kiddie",
  "respect": 3,
  "total_challenges": 6,
  "profile_picture": "https://www.hackthebox.eu/storage/avatars/3158e2cf3b6b5488441e02b72b0374d7.png",
  "username": "Magnussen",
  "respected_by": [
    {
      "profile_picture": "https://www.hackthebox.eu/storage/avatars/e8111c3c228dd421dc7769bfb3d25a3a.png",
      "username": "Kppucino"
    },
    {
      "profile_picture": "https://www.hackthebox.eu/storage/avatars/6ea3a1fb1b28c8f31ff7d977d1ab8b2b.png",
      "username": "switch"
    },
    {
      "profile_picture": "https://www.hackthebox.eu/storage/avatars/64a11b2aced4e6bea0d3eafd2c27e277.png",
      "username": "nlegall"
    }
  ],
  "rank": 799,
  "owned_users": 4
}
```

## Installing

First you have to clone this repo :

```
git clone https://github.com/magnussen7/htb-api.git
```

Then you can create a virtualenv and install the mandatory packages.

```
cd htb-api/
pip install -r requirements.txt
```

You can now run the api with :

```
python3 api.py
```

If you want to use the API in production you should run it with Nginx, all WSGI files are available in this repository.

Nginx configurations example :

```
> cat /etc/nginx/sites-available/api_htb.com.conf
server 
{
    listen 80;
    server_name api_htb.com www.api_htb.com;
    
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/path/to/api/folder/api_htb.sock;
    }}

> sudo ln -s /etc/nginx/sites-available/api_htb.com.conf /etc/nginx/sites-enabled
> sudo service nginx restart
```

Don't forget to change the server name and the path to the socket.
Of course, it's highly recommended to set a certificate.

### Help for Flask server in production

- [https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)

## Authors

- **Magnussen**


