import logging
import random

from fastapi import APIRouter
from fastapi import HTTPException

from app.api import api
from app.model.Message import Message

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/hello")
def hello(name: str):
    """
    This function is an endpoint for the GET request at the "/hello" route. It takes in a parameter name of type str, representing the name of the person to greet. It returns a JSON response with a "message" field containing a greeting message in the format "Hello {name}!".

    Parameters:

        name (str): The name of the person to greet.

    Returns:

        dict: A JSON response containing a greeting message.

    Example:

        GET /hello?name=John

    Response:

        {"message": "Hello John!"}
    """
    logger.info("called 'hello' endpoint")
    return {"message": f"Hello {name}!"}


@router.get(
    "/message",
    summary="Random Halloween Message",
    response_model=Message,
)
def get_message():
    """
    This function is an endpoint for the GET request at the "/message" route. It will returns one random halloween message.

    Parameters:

        name (str): The name of the person to greet.

    Returns:

        dict: A JSON response containing a greeting message.

    Example:

        GET /message
    """
    logger.info("called 'message' endpoint")
    messages = api.get_messages()
    return random.choice(messages)


@router.get("/location",
            summary="Get the details of spooky site nearest to you")
def nearest_spooky_site(station: str):
    """
    This function is an endpoint for the GET request at the "/location" route. It will return the location
    and details of the nearest spooky site based on the provided MRT station name.
    Parameters:

        station (str): The name of MRT station

    Returns:

        dict: A JSON response containing the details of the nearest spooky site.

    Example:

        GET /location?station=pioneer
    """
    if not station:
        raise HTTPException(status_code=400,
                            detail="Please enter valid string")
    if not station.istitle():
        raise HTTPException(
            status_code=400,
            detail="Station name must be in title case (e.g., 'Clarke Quay')")
    try:
        spooky_site_details = api.nearest_spooky_site(station)
        return spooky_site_details
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/flag")
def flag():
    """
    This function is an endpoint for the GET request at the "/flag" route.

    Returns:
    str: The flag obtained from the "api.print_secret()" function.
    """
    return api.print_secret()
