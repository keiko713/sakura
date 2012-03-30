[SAKURA PHOTOS](http://sakura.playshiritori.com/)
==========

Let's look at beautiful Japanese SAKURA pictures from Twitter!

This application shows the photos that were tweeted with #桜2012 hash tag.



Quick start
----------

 * Clone the repo using the command `git clone git@github.com:keiko713/sakura.git`
 * You need to make api_keys.py and add `FLICKR_API_KEY = 'your flickr API key'` in order to get the photos from flickr
 * Run `python manage.py syncdb` in order to make sqlite database
 * Run `python manage.py runserver`, now you can see the app at http://localhost:8000/



Copyright and license
----------
Copyright 2012 [Keiko Oda](http://twitter.com/keiko713)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this work except in compliance with the License.
  You may obtain a copy of the License in the LICENSE file, or at:

   <http://www.apache.org/licenses/LICENSE-2.0>

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
