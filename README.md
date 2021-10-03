# Reddit Clone - built with Django

## Interactions - What user can do

### ```Subreddits```
User can create it, upload photo to its profile, join/left community, create posts in it.
### ```Posts```
User can make it in any subreddit, they can delete it, upvote/downvote, also they can comment it.
### ```Comments```
User can create it in any post, reply to existing, delete and upvote/downvote.
### ```User profile```
User can see all activity that some user has done, their posts, comment, their bio description.

If its their profile, they can also upload profile picture, update existing, create or update their bio description, see upvotes/downvotes they have done.

### ```Notifications```
User can see all posts/comments that other users interacted with.

## How things are done
### ```Karma```
Whenever user get upvote or downvote, it chages his karma.
User can't interact with his own karma, but his upvote/downvote will be taken into account.
It created with the help of django signals, so everytime user creates vote, it makes signal to either add or decrement from users karma. 
### ```Upvote/Downvote```
Whenever user do vote, it check whether opposite vote exists or not, so it can delete it. So if user already upvoted comment a, and then he decided to revote, it will remove already existed upvote and create downvote.
After vote is created, it creates signal to interact with objects creator karma.
### ```Comment```
Nested comments is made with the help of Django MPTT library.
### ```Notifications```
When user comments your posts, upvote/ downvote it you recieve notification.
Also when user replies to your comment, upvote/downvote it, you recieve notifications.

If ypu will interact with your content, you won't recieve any notification.
Also if you recieve a notification and user decided to remove his content or he revoted, you won't recieve new notification.

## Technologies used:
### Frontend
```
HTML
CSS
Django Templates
Vanilla JavaScript
```
### Backend
```
Django Framework
Django MPTT
Django Signals
SQLite3
Pillow
```

## Instruction to run this project

1. You need to dl/clone this repository to your device.
2. Activate your virtualenv.
3. Run ```pip install -r requirements.txt``` in your shell.
4. Connect your database in ```cna/settings.py```.
5. Run migraions: type in your shell ```python manage.py makemigrations``` and ```python manage.py migrate```.
6. Run ```python manage.py runserver``` in your shell.
7. All done!
