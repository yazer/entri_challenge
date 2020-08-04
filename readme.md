### Overview
Portal for scheduling interviews. Interviewer and candidiate can register their available 
time slot. Multiple interviews can happen at a time and both candidate and interviewer can book any number of slots. Matching slots will be retrieved according to the candidate and interviewer ids. 


1. CANDIDATE REGISTRATION

        End point for registering candidates for interview

        POST: /user-management/register-candidate/
        Request: 
            {
                "first_name": "Yakzen",
                "last_name": "Periera",
                "email": "yakzengarryperiera@gmail.com",
                "phone_number": "9988776655",
                "password": "yakzen123"
            } 


2. INTERVIEWER REGISTRATION

        End point for registering interviewer

        POST: /user-management/register-interviewer/ 
        Request: 
            {
                "first_name": "Rex",
                "last_name": "Vijayan",
                "email": "rexvijayan@gmail.com",
                "phone_number": "9876598765",
                "password": "rexvijayan123"
            }


3. USER LOGIN

        End point for interviewer/candidate login

        POST: /user-management/login/
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

        End point for booking slots for candidate/interviewer

        Assumptions:
            1.Assuming each slot will be datetime of 1 hour duration. So from datetime date and time slot is captured.
            2.Any number of slots can be booked by both candidate and interviewer
            3.Multiple interviews can happen at a time. So multiple users can book same slots.
            4.Date format should be as specified below

        POST: /user-management/book-slot/
        
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

        End point for getting available time slots for interview.
    
        GET: /user-management/get-availability/?cid=9&iid=22
        
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


6. CANDIDATE LIST

        End point for getting candidate list
    
        GET: /user-management/candidate-list/
        
        Response:
            [
                {
                    "id": 9,
                    "first_name": "Yakzen",
                    "phone_number": "9988776655",
                    "email": "yakzengarryperiera@gmail.com"
                },
                {
                    "id": 10,
                    "first_name": "Rex",
                    "phone_number": "9876598765",
                    "email": "rexvijayan@gmail.com"
                }
            ]

    
7. INTERVIEWER LIST

        End point for getting interviewer list
    
        GET: /user-management/interviewer-list/
        
        Response:
            [
                {
                    "id": 21,
                    "first_name": "Santhosh",
                    "phone_number": "9876554321",
                    "email": "santhoshnarayan@gmail.com"
                },
                {
                    "id": 22,
                    "first_name": "Anirudh",
                    "phone_number": "9879876543",
                    "email": "anirudhravichander@gmail.com"
                }
            ]