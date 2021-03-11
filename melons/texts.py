usrnm_errmsg_require = "* Please enter your username"
usrnm_errmsg_length = "* Username length must between 6-150 characters"
usrnm_errmsg_exist = "* Username already exists, please try again or login"
usrnm_errmsg_NOT_exist = "* Cannot find your account"
usenm_helptxt = "Use 6 or more characters (combination of letters and numbers)"


paswd_errmsg_require = "* Please enter your password"
paswd_errmsg_length = "* Password length must more than 8 characters"
paswd_errmsg_mismatch = "* Passwords not match, please try again"
paswd_helptxt = "Use 8 or more characters (combination of letters, numbers, and symbols)"

unpw_errmsg_mismatch = "* Username and password do not match, please try again"

name_errmsg_require = "* Please enter your name"
name_errmsg_length = "* Name length (for both fields) must under 150 characters"

email_errmsg_style = "* Invalid email address, please try again"
email_errmsg_require = "* Please enter your email"
email_errmsg_exist = "* Email already exists, please try again or login "

expense_record_text = "[{exp_type}] Item-{item_id} with {exp_amount} gold at {exp_time}"


def expense_record(exp_type, item_id, exp_amount, exp_time):
    return expense_record_text.format(exp_type, item_id, exp_amount, exp_time)
