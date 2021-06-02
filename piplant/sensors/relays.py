import RPi.GPIO as GPIO

from piplant.settings import settings

from fastapi import APIRouter, HTTPException, Response

router = APIRouter(tags=['relays'])

__not_found_error = {
    'status_code': 404,
    'detail': 'Relay not found'
}


async def toggle_relay(pin: int, state: bool) -> bool:
    for relay in settings.relays:
        if relay.pin == pin:
            value = state
            if relay.active_low:
                value = not state

            GPIO.setup(pin, GPIO.OUT, initial=value)
            return True

    return False


@router.post('/relay/{pin}/off', status_code=204)
async def turn_off_relay(pin: int):
    """
    Attempts to turn off the specified relay. It takes in account whether the relay is active low or not.
    :param pin: GPIO pin used to control the relay
    :return: 204 if successful. 404 if a relay connected to that pin was not found.
    """
    if not await toggle_relay(pin, False):
        raise HTTPException(**__not_found_error)
    else:
        return Response(status_code=204)


@router.post('/relay/{pin}/on', status_code=204)
async def turn_on_relay(pin: int):
    """
        Attempts to turn on the specified relay. It takes in account whether the relay is active low or not
        :param pin: GPIO pin used to control the relay
        :return: 204 if successful. 404 if a relay connected to that pin was not found.
        """
    if not await toggle_relay(pin, True):
        raise HTTPException(**__not_found_error)
    else:
        return Response(status_code=204)
