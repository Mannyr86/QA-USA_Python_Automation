import json
import time
import ssl
import urllib.request
import logging
from selenium.common.exceptions import WebDriverException, TimeoutException
from urllib.error import URLError

# Set up logging
logging.basicConfig(level=logging.INFO)


def retrieve_phone_code(driver) -> str:
    """
    Retrieves the phone confirmation code from browser logs using CDP.

    Use this only after the code is requested in the application.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        str: Phone confirmation code.

    Raises:
        TimeoutException: If the code is not found within the retry limit.
    """
    for attempt in range(1, 11):  # Retry 10 times
        try:
            # Fetch browser logs related to phone number confirmation API
            logs = [
                log["message"]
                for log in driver.get_log('performance')
                if log.get("message") and 'api/v1/number?number' in log["message"]
            ]
            if logs:
                for log in reversed(logs):
                    message_data = json.loads(log)["message"]
                    body = driver.execute_cdp_cmd(
                        'Network.getResponseBody',
                        {'requestId': message_data["params"]["requestId"]}
                    )
                    body_str = body.get('body', '') if body else ''
                    if isinstance(body_str, str) and body_str:
                        code = ''.join(filter(lambda c: c.isdigit(), body_str))
                        if code:
                            logging.info(f"Phone code found: {code}")
                            return code  # Return code as soon as it's found
        except WebDriverException as e:
            logging.warning(f"Attempt {attempt}: WebDriverException occurred: {str(e)}. Retrying...")
            time.sleep(1)
        except Exception as e:
            logging.error(f"An unexpected error occurred during code retrieval: {str(e)}")
            raise TimeoutException("Timeout while trying to retrieve phone confirmation code.")

    # Raise exception if the code is not found after 10 attempts
    raise TimeoutException(
        "Phone confirmation code not found after 10 attempts. Make sure the code was requested in the application."
    )


def is_url_reachable(url: str) -> bool:
    """
    Checks if the given URL is reachable.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if reachable, False otherwise.
    """
    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx) as response:
            return response.status == 200
    except URLError as e:
        logging.error(f"URL check failed: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return False
