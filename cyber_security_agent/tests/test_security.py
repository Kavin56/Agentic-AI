import pytest
import requests

BASE_URL = "https://taupe-tanuki-66c44a.netlify.app"

# Test for SQL Injection
@pytest.mark.security
def test_sql_injection():
    payload = "' OR '1'='1"
    response = requests.get(f"{BASE_URL}/?query={payload}")
    
    assert response.status_code != 200, "Possible SQL Injection detected!"

# Test for XSS
@pytest.mark.security
def test_xss():
    payload = "<script>alert('XSS')</script>"
    response = requests.get(f"{BASE_URL}/?query={payload}")

    assert payload not in response.text, "Possible XSS vulnerability found!"

# Test for Security Headers
@pytest.mark.security
def test_security_headers():
    response = requests.get(BASE_URL)

    assert "X-Frame-Options" in response.headers, "X-Frame-Options missing!"
    assert "X-Content-Type-Options" in response.headers, "X-Content-Type-Options missing!"
    assert "Content-Security-Policy" in response.headers, "Content-Security-Policy missing!"

# Test for Open Redirect
@pytest.mark.security
def test_open_redirect():
    payload = "https://evil.com"
    response = requests.get(f"{BASE_URL}/redirect?url={payload}", allow_redirects=False)

    assert response.status_code not in [301, 302], "Possible Open Redirect vulnerability detected!"
