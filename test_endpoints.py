import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_max_sum():
    """Test max sum endpoint"""
    data = {"numbers": [1, 2, 3, 4, 5], "k": 3}
    response = requests.post(f"{BASE_URL}/max-sum", json=data)
    assert response.status_code == 200
    assert response.json()["max_sum"] == 12
    print("✅ Max sum test passed")

def test_two_sum():
    """Test two sum endpoint"""
    data = {"values": [2, 7, 11, 15], "target": 9}
    response = requests.post(f"{BASE_URL}/Two-sum", json=data)
    assert response.status_code == 200
    assert response.json()["indices"] == [0, 1]
    print("✅ Two sum test passed")

def test_palindrome():
    """Test palindrome endpoint"""
    data = {"s": "racecar"}
    response = requests.post(f"{BASE_URL}/palindromechecker", json=data)
    assert response.status_code == 200
    assert response.json()["is_palindrome"] == True
    print("✅ Palindrome test passed")

if __name__ == "__main__":
    print("Running API tests...")
    try:
        test_max_sum()
        test_two_sum()
        test_palindrome()
        print("🎉 All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")