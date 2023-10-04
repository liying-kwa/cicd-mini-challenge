# DO NOT EDIT, NOT PART OF CHALLENGE

from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.api import api
from dotenv import load_dotenv
import os

from app.model.Station import Station
from app.model.Message import Message

load_dotenv()
client = TestClient(app)


# This test function checks the "/hello" endpoint with different inputs
# It asserts that the response status code is 200 (HTTP OK) and
# the JSON body of the response is as expected for each input
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("john", {"message": "Hello john!"}),
        ("alice", {"message": "Hello alice!"}),
        ("bob", {"message": "Hello bob!"}),
    ],
)
def test_hello(test_input, expected):
    response = client.get("/hello", params={"name": test_input})
    assert response.status_code == 200
    assert response.json() == expected


# This test function mocks the read_json function to return a specific output
# Then it asserts that the mock was called with the correct argument,
# the get_messages function returns a list of Message objects, and
# these objects are the expected ones
@patch(
    "app.api.api.read_json",
    return_value=[{"id": "1", "message": "abc"}, {"id": "2", "message": "xyz"}],
)
def test_get_messages(mock_read_json):
    message = api.get_messages()
    mock_read_json.assert_called_once_with("data/message.json")
    assert isinstance(message, list)
    assert all(isinstance(item, Message) for item in message)
    expected_messages = [Message(id="1", message="abc"), Message(id="2", message="xyz")]
    assert message == expected_messages


# This test function mocks the read_json function to return an empty list
# Then it asserts that the mock was called with the correct argument,
# and the get_messages function returned an empty list
@patch("app.api.api.read_json", return_value=[])
def test_get_messages_empty_json(mock_read_json):
    messages = api.get_messages()
    mock_read_json.assert_called_once_with("data/message.json")
    # Assert that the function returned an empty list
    assert isinstance(messages, list)
    assert len(messages) == 0


# This test function checks the "/message" endpoint
# It asserts that the response status code is 200 (HTTP OK)
# and the JSON body of the response is not empty
def test_get_message():
    response = client.get("/message")
    assert response.status_code == 200
    assert response.json()


# This test function Retrieve latitude and longitude for a station.
# Test the correct retrieval of latitude and longitude for the station 'Rochor'.
# Test that a 'ValueError' is raised when retrieving a non-existent station, 'treepoint'.
def test_get_latlong():
    station_list = [
        Station(station_name="Rochor", type="MRT", lat=1.303601, lng=103.852581),
        Station(station_name="Compassvale", type="LRT", lat=1.394615, lng=103.900443),
    ]
    latitude, longitude = api.get_latlong("Rochor", station_list)
    assert latitude == 1.303601
    assert longitude == 103.852581

    with pytest.raises(ValueError):
        api.get_latlong("treepoint", station_list)  # There is no treepoint in the list


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "Redhill",
            {
                "name": "The Abandoned Mansion at Telok Blangah Rise",
                "area": "South",
                "nearest_mrt": "Telok Blangah",
            },
        ),
        (
            "Paya Lebar",
            {
                "name": "The Haunted Well of Bedok Reservoir",
                "area": "East",
                "nearest_mrt": "Bedok Reservoir",
            },
        ),
        (
            "Simei",
            {
                "name": "The Cursed Alley behind Tampines Mall",
                "area": "East",
                "nearest_mrt": "Tampines",
            },
        ),
        (
            "Little India",
            {
                "name": "The Ghostly Theatre at Dhoby Ghaut Green",
                "area": "Central",
                "nearest_mrt": "Dhoby Ghaut",
            },
        ),
        (
            "Serangoon",
            {
                "name": "The Whispering Woods of Bishan Park",
                "area": "Central",
                "nearest_mrt": "Bishan",
            },
        ),
        (
            "Punggol",
            {
                "name": "The Forbidden Shrine near Hougang Plaza",
                "area": "North-East",
                "nearest_mrt": "Hougang",
            },
        ),
    ],
)
# This test function check if the API returns the correct information for the nearest spooky site based on the input station.
# It uses pytest.mark.parametrize to run multiple test cases with different input and expected output.
def test_nearest_spooky_site(test_input, expected):
    response = client.get("/location", params={"station": test_input})
    assert response.status_code == 200
    assert response.json() == expected

# This test function checks the behavior of the API when an invalid station name is provided as input.
# It uses pytest.mark.parametrize to run multiple test cases with different invalid station names.


@pytest.mark.parametrize("test_input", ["Habourfront", "Sangkeng", "Lily"])
def test_nearest_spooky_site_invalid_station(test_input):
    response = client.get("/location", params={"station": test_input})
    assert response.status_code == 400
    response_json = response.json()  # Parse the JSON response
    assert "detail" in response_json  # Check if "detail" key exists in the response JSON
    assert response_json["detail"] == f"No station found with the name {test_input}"

# This test function check the behavior of the API when an invalid station name (not in title case) is provided as input.
# It uses pytest.mark.parametrize to run multiple test cases with different invalid station names.


@pytest.mark.parametrize("test_input", ["JURONG WEST", "sengkang", "oRchard"])
def test_nearest_spooky_site_invalid_station_not_title_case(test_input):
    response = client.get("/location", params={"station": test_input})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Station name must be in title case (e.g., 'Clarke Quay')"
    }


# This test function check the behavior of the API when no station name is provided as input.
# It tests if the API returns a 400 status code and a specific error message when the "station" parameter is missing.
def test_nearest_spooky_site_without_station():
    response = client.get("/location?station=")
    assert response.status_code == 400  # As station param is required
    assert response.json() == {"detail": "Please enter valid string"}


# Protected Router
def test_protected_with_valid_api_key():
    """
    Test the /protected endpoint with a valid API key.
    Expect a 200 OK response.
    """

    api_key = os.getenv("API_KEY")
    headers = {"X-API-Key": api_key}
    resp = client.get("/secret", headers=headers)

    assert resp.status_code == 200
    # Add additional assertion on the response body if applicable.
    # assert resp.json() == {"message": "Authorized"}


def test_protected_with_invalid_key():
    """
    Test the /protected endpoint with an invalid API key.
    Expect a 401 Unauthorized response.
    """

    headers = {"X-API-Key": "INVALID_API_KEY"}
    resp = client.get("/secret", headers=headers)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Invalid API key"}
