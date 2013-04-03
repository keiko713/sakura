[SAKURA PHOTOS](http://sakura.playshiritori.com/)
==========

Let's look at beautiful Japanese SAKURA pictures from Twitter!

This application shows the photos that were tweeted with #桜2013 hash tag.



Quick start
-----------

 * Install pip (skip if you already have). `[sudo] easy_install pip`
 * Install virtualenv (skip if you already have). `[sudo] pip install virtualenv`
 * Clone (or Fork and Clone) the repo `git clone git://github.com/keiko713/sakura.git` or `git clone git@github.com:[yourusername]/sakura.git`
 * `cd` to `sakura` folder and create a virtualenv `virtualenv venv --distribute`
 * Activate the virtualenv `source venv/bin/activate`
 * (Optional) Install libjpeg for jpeg support of PIL `brew install libjpeg`
 * Install dependencies on the virtualenv `pip install -U -r requirements.txt`
 * Set following environament variables
   * `export FLICKR_API_KEY=yourapikey` (You can get it from [here](http://www.flickr.com/services/api/keys/))
   * `export TWITTER_OAUTH_TOKEN=youroauthtoken` (You can get them from [here](https://dev.twitter.com/apps), you need to create a new application)
   * `export TWITTER_OAUTH_SECRET=youroauthsecret`
   * `export TWITTER_CONSUMER_KEY=yourconsumerkey`
   * `export TWITTER_CONSUMER_SECRET=yourconsumersecret`
 * Run your postgresql database, create sakura user and sakuraphotos database (you can change the name, but if you change it, you should change var in sakura/settings.py also)
   * `psql`
   * `CREATE USER sakura WITH ENCRYPTED PASSWORD 'sakura';`
   * `CREATE DATABASE sakuraphotos` ENCODING 'UTF8' OWNER sakura;`
 * Run `python manage.py syncdb`
 * Run `python manage.py runserver`, now you can see the app at http://localhost:8000/



Deploying on Heroku
-------------------

You can deploy SAKURA PHOTOS on Heroku easily.
 * Clone (or Fork and Clone) the repo `git clone git://github.com/keiko713/sakura.git` or `git clone git@github.com:[yourusername]/sakura.git`
 * `cd` to `sakura` folder
 * `heroku create` (I assume you've already done Step 1 to 3 in this [doc](https://devcenter.heroku.com/articles/quickstart))
 * Change app name with `heroku apps:rename newname` if you want (see [here](https://devcenter.heroku.com/articles/renaming-apps) for detail)
 * Set all config variables
   * `heroku config:add FLICKR_API_KEY=yourkey`
   * `heroku config:add TWITTER_OAUTH_TOKEN=yourkey`
   * `heroku config:add TWITTER_OAUTH_SECRET=yourkey`
   * `heroku config:add TWITTER_CONSUMER_KEY=yourkey`
   * `heroku config:add TWITTER_CONSUMER_SECRET=yourkey`
 * Change the buildpack for Coffeescript support (I'm using this buildpack temporary, since it's the one works for me)
   * `heroku config:add BUILDPACK_URL=git://github.com/tmandry/heroku-buildpack-django.git`
 * `git push heroku master`
 * `heroku ps:scale web=1`
 * `heroku open` or just visit `http://yourappname.herokuapp.com/` on the browser
 * DONE!


Copyright and license
----------
Copyright 2013 [Keiko Oda](http://twitter.com/keiko713)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this work except in compliance with the License.
  You may obtain a copy of the License in the LICENSE file, or at:

   <http://www.apache.org/licenses/LICENSE-2.0>

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
