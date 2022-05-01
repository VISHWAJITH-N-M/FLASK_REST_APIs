import json
import mysql.connector
import flask
from flask import Flask, jsonify, request
import random

app = Flask(__name__)

mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
        )

mycursor = mydb.cursor()
mycursor.execute("use bank;")

@app.route('/')

def hello_world():
    return 'Eunimart'

@app.post('/signup')

def signup():
    signup_get_details = json.loads(request.data)
    query = "select mobile_num from signup where mobile_num = {}".format(signup_get_details['mobile'])
    mycursor.execute(query)
    try:
        temp = mycursor.fetchone()[0]
        print(temp)
        return { "message": "Account already exists" }
    except TypeError:
        otp = random.randint(1111, 9999)
        query = "insert into signup (country_code, mobile_num, first_name, last_name, otp) values({}, {}, '{}', '{}', {});".format(
        signup_get_details["code"], signup_get_details["mobile"], signup_get_details["fname"], signup_get_details["lname"], otp)
        mycursor.execute(query)
        mydb.commit()
        return { "message": "OTP sent" }

@app.route('/verify', methods = ['POST'])
def verify():
    get_verify_details = json.loads(request.data)
    query = "select mobile_num from signup where mobile_num = {}".format(get_verify_details['mobile'])
    mycursor.execute(query)
    try:
        temp = mycursor.fetchone()[0]
        print(temp)
        query = "select verified from signup where mobile_num = {} ".format(get_verify_details["mobile"])
        mycursor.execute(query)

        verify_check = mycursor.fetchone()[0]

        if verify_check == 0:

            query = "select otp from signup where mobile_num = {} ".format(get_verify_details["mobile"])
            mycursor.execute(query)
            check_otp = mycursor.fetchone()[0]
            try:
                if check_otp == get_verify_details['entered_otp']:
                    query = "update signup set verified = 1 where mobile_num = {}".format(get_verify_details["mobile"])
                    mycursor.execute(query)
                    mydb.commit()
                    return { "message": "Verified successfully" }
                else:
                    return { "error": "Invalid OTP" }
            except KeyError:
                return { "error": "Invalid OTP" }
        else:
            return { "message": "Verified already" }
    except TypeError:
        return { "error": "Sign up required" }

@app.post('/account')
def account():
    get_account_details = json.loads(request.data)
    query = "select * from signup where mobile_num = '{}'".format(get_account_details["mobile"])
    mycursor.execute(query)
    all = mycursor.fetchall()
    print(all)
    if len(all) == 1:
        verify = all[0][5]
        if verify == 1:
            fname = all[0][2]
            lname = all[0][3]
            query = "select mobile_num from account_details where mobile_num = '{}'".format(get_account_details['mobile'])
            mycursor.execute(query)
            try:
                temp = mycursor.fetchone()[0]
                return { "message": "Account already exists" }
            except:
                query = "INSERT INTO `account_details`(`fname`, `lname`, `father_name`, `perm_add`, `curr_add`, `dob`, `mobile_num`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(
                    fname,lname,get_account_details['father'],get_account_details['perm'],get_account_details['curr'],get_account_details['dob'],get_account_details['mobile'])
                mycursor.execute(query)
                mydb.commit()
                return { "message": "Account Created" }
        else:
            return { "message": "Verification required" }
    else:
        return { "error": "Given number doesn't exist" }


if __name__ == '__main__':
    app.run()


#
# countries_and_states = {
#     "91": [
#         "Tamil Nadu",
#         "Kerala"
#     ]
# }