# Social Networking API with Django Rest Framework
Django Rest Framework with social networking, searching, signup, login


## Setup & Run DRF Server
1. Clone this repo or copy page below command  
`git clone https://github.com/imvishvaraj/drf-social-networkig.git`

2. Create virtual environment for project  
`virtualenv -p python3 venv`

3. Activate virtual environment  
`source venv/bin/activate`

4. Install python dependencies  
`pip install -r social_network/requirements.txt`

5. Apply Database Migrations  
`python manage.py migrate`

6. Run Django Server  
`python manage.py runserver`

7. Now you can access API endpoints via Postman or Curl calls.


## API Endpoints:
All API endpoints need Authorization Header. Except register, login.
- Register a new user: `POST /users/register/`
- Login a user: `POST /users/login/`
- Current user details: `GET /users/me/`
- Search users: `GET /users/search/`
    - Pass email param to search by email id:  
     `GET /users/search/?email=yoda@example.com`
    - Pass name param to search user by name  
    `GET /users/search/?name=pa`
- Friend Requests:
    - Send: `POST /friends/requests/ -d {"to_user": 1}`
    - Accept: `POST /friends/requests/<user_id:int>/accept/`
    - Reject: `POST /friends/requests/<user_id:int>/reject/`
    - List Pending Requests: `GET /friends/requests/pending/`
- List Friends: `GET /friends/<user_id:int>/`

