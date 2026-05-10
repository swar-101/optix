from SmartApi import SmartConnect
import pyotp


def get_angel_one_session(config):
    cred    = config['Credentials'][0]
    obj     = SmartConnect(api_key=cred['API_Key'])
    totp    = pyotp.TOTP(cred['totp_key']).now()
    session = obj.generateSession(cred['ClientID'], cred['Password'], totp)
    if session['status']:
        print("✅ Login Successful!")
        return obj
    print("❌ Login Failed")
    return None