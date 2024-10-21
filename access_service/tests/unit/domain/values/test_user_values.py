import pytest
from uuid import uuid4

from access_service.domain.exceptions.user import (
    InvalidPasswordError,
    InvalidPhoneNumberError, 
    InvalidUsernameError
)

from access_service.domain.values.user import (
    UserID,
    UserPhoneNumber,
    UserName,
    UserRawPassword
)

def test_user_id():
    uuid = uuid4()
    user_id = UserID(uuid)

    assert uuid == user_id.to_raw()


@pytest.mark.parametrize(
    "phone_number, exception",
    [
        ("+71234567890", None),  
        ("+7123456789", InvalidPhoneNumberError),   
        ("+7123456789a", InvalidPhoneNumberError), 
        ("+7123456789-", InvalidPhoneNumberError),  
        ("81234567890", InvalidPhoneNumberError),  
        ("+7123456789012", InvalidPhoneNumberError),
    ]
)
def test_user_phone_number(
    phone_number,
    exception,
):
    if exception is None:
        user_phone_number = UserPhoneNumber(phone_number)
        assert phone_number == user_phone_number.to_raw()
    else:
        with pytest.raises(exception):
            UserPhoneNumber(phone_number)


@pytest.mark.parametrize(
    "username, exception",
    [
        ("abcd", None),                      
        ("a1234", None),                      
        ("A_user.name", None),               
        ("Z1234_5678.abcdef", None),         
        ("AbCdEf12345", None),               
        ("12345", InvalidUsernameError),       
        ("_abcd", InvalidUsernameError),       
        ("ab", InvalidUsernameError),         
        ("abcde!", InvalidUsernameError),     
        ("aVeryLongUserNameThatIsWayTooLong12345", InvalidUsernameError), 
    ]
)
def test_username(
    username,
    exception
):
    if exception is None:
        user_name = UserName(username)
        assert username == user_name.to_raw()
    else:
        with pytest.raises(exception):
            user_name = UserName(username)


@pytest.mark.parametrize(
    "password, exception",
    [
        ("Abcdef1!", None),                    
        ("StrongPass1$", None),               
        ("A1b2C3d4@", None),                  
        ("Password1!", None),                 
        ("Aa1!Aa1!Aa1!", None),               
        ("abcdefg", InvalidPasswordError),      
        ("ABCDEFG1", InvalidPasswordError),     
        ("abcDEF12", InvalidPasswordError),     
        ("Ab1!", InvalidPasswordError),         
        ("password", InvalidPasswordError),     
        ("12345678!", InvalidPasswordError),    
    ]
)
def test_raw_password(
    password,
    exception,
): 
    if exception is None:
        raw_password = UserRawPassword(password)
        assert password == raw_password.to_raw()
    else:
        with pytest.raises(exception):
            raw_password = UserRawPassword(password)