
from app.auth import API_KEY, verify_api_key


def test_api_key_configuration():

    assert API_KEY != ""

    assert API_KEY == "my_secret_chat_key_123"

    print("API key loaded successfully!")

    
def test_auth_function_exists():

    assert callable(verify_api_key)

    print("Authentication function available!")


if __name__ == "__main__":

    test_api_key_configuration()

    test_auth_function_exists()

    print("All authentication configuration tests passed!")
