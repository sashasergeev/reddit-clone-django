# Reddit Clone - built with Django

[Live DEMO](https://redditclonedjango.herokuapp.com)

Static and media files are powered with [AWS S3](https://aws.amazon.com/ru/s3/).

---

## **How things are done**
### ***Karma***
Whenever user get upvote or downvote, it chages his karma.
User can't interact with his own karma, but his upvote/downvote will be taken into account.
It created with the help of django signals, so everytime user creates vote, it makes signal to either add or decrement from users karma. 
### ***Upvote/Downvote***
Whenever user do vote, it check whether opposite vote exists or not, so it can delete it. So if user already upvoted comment a, and then he decided to revote, it will remove already existed upvote and create downvote.
After vote is created, it creates signal to interact with objects creator karma.

### ***Comment***
Nested comments is made with the help of Django MPTT library.

Also, posts are paginated with infinite scroll.
### ***Notifications***
When user comments your posts, upvote/ downvote it you recieve notification.
Also when user replies to your comment, upvote/downvote it, you recieve notifications.


If you will interact with your content, you won't recieve any notification.
Also if you recieve a notification and user decided to remove his content or he revoted, you won't recieve new notification.

...

___

## **Interactions - What user can do**

### **Subreddits**
- create
- if admin, he can set it up
- join
- left
- create post in it

### **Posts**
- sort it by date
- create
- save
- delete
- upvote
- downvote
- comment

### **Comments**
- create
- reply 
- delete
- save
- downvote
- comment
### **User profile**

- see activity
- see profile

If it is their profile:
- set up profile
- see upvotes/downotes, saved material

### **Notifications**
- gets it whenever someone is interacted with their posts/comments.

### **Search functionality**
- search for : 
    - subreddit
    - post
    - user
- live search (just results that displayed instantly on navbar) for: 
    - subreddit

***

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
Django Heroku 
Django Signals
SQLite3
Pillow
Django MPTT - used for making nested comments
Django Storages - used for managing static and media files on AWS S3 servers.
```

## Instruction to run this project

1. You need to dl/clone this repository to your device.
2. Activate your virtualenv.
3. Run ```pip install -r requirements.txt``` in your shell.
4. Connect your database in ```cna/settings.py```.
5. Run migraions: type in your shell ```python manage.py makemigrations``` and ```python manage.py migrate```.
6. Run ```python manage.py runserver``` in your shell.
7. All done!
