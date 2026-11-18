# import page


class LocatorAdminSignin:
    #email id
    login_email_id = "input[name='email']"
    #password
    login_password = "input[type='password']"
    #login button
    login_button = {"role": "button", "name": "Login"}

    #Validate that the SmartRecruit logo in top-left is available or not!
    SMART_RECRUIT_LOGO = "Smart Recruit"