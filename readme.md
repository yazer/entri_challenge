1. CANDIDATE REGISTRATION

Overview: Candidate registration

URL: http://127.0.0.1:8000/user-management/register-candidate/
Method: POST
Request: 
    {
        "first_name": "Yakzen",
        "last_name": "Periera",
        "email": "yakzengarryperiera@gmail.com",
        "phone_number": "9988776655",
        "password": "yakzen123"
    } 


2. INTERVIEWER REGISTRATION

Overview: Interviewer registration

URL: http://127.0.0.1:8000/user-management/register-interviewer/ 
Method: POST
Request: 
    {
        "first_name": "Rex",
        "last_name": "Vijayan",
        "email": "rexvijayan@gmail.com",
        "phone_number": "9876598765",
        "password": "rexvijayan123"
    }


3. USER LOGIN

Overview: Login for both candidate and interviewer

URL: http://127.0.0.1:8000/user-management/login/
Method: POST
Request:
    {
        "username":"9988776655",
        "password": "yakzen123"
    }

Response:
    Success: {
                "token": "e01eceb1fcd43923e889c4364dd891091ad7c8f0"
            }
    Failed: {
                "msg": "Incorrect username or password"
            }


4. SLOT BOOKING

Overview: Slot booking for both candidate and interviewer

URL: http://127.0.0.1:8000/user-management/book-slot/
Method: POST

Assumptions:
    1.Assuming each slot will be datetime of 1 hour duration. So from datetime date and time slot is captured.
    2.Any number of slots can be booked by both candidate and interviewer
    3.Multiple interviews can happen at a time. So multiple users can book same slots.
    4.Date format should be as specified below

Request:
    {
        "slot":["2020-08-05 09:00:00.000000", 
                "2020-08-05 10:00:00.000000",
                "2020-08-05 11:00:00.000000",
                "2012-09-05 16:00:00.000000",
                "2020-08-05 17:00:00.000000", 
                "2020-08-06 08:00:00.000000",
                "2020-08-06 12:00:00.000000",
                "2020-08-06 19:00:00.000000",
                "2012-09-06 20:00:00.000000"
                ]
    }


5.VIEW AVAILABITY

Overview: Get list of common slots , given candidate id and interviewer id.

URL: http://127.0.0.1:8000/user-management/get-availability/?cid=9&iid=22
Method: GET

Response:
    {
        "response": [
            {
                "date": "2020-08-05",
                "slot": [
                    "09:00:00",
                    "10:00:00"
                ]
            },
            {
                "date": "2020-08-06",
                "slot": [
                    "19:00:00"
                ]
            }
        ]
    }