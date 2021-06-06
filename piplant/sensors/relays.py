import RPi.GPIO as GPIO

from typing import List

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from piplant.database import pool

router = APIRouter(tags=['relays'])

__not_found_error = {
    'status_code': 404,
    'detail': 'Relay not found'
}


class RelayModel(BaseModel):
    pin: int
    name: str
    active_low: bool


class RelayStateModel(RelayModel):
    on: bool


async def get_relay(pin: int):
    async with pool.pool.acquire() as connection:
        stmt = await connection.prepare('SELECT pin, name, active_low FROM relays WHERE pin = $1')
        data = await stmt.fetch(pin)

        if data is not None:
            return RelayModel(**data[0])
        else:
            return None


async def toggle_pin(pin: int, active_low: bool, state: bool):
    if active_low:
        state = not state

    GPIO.setup(pin, GPIO.OUT, initial=state)


async def toggle_relay(relay: RelayModel, state):
    value = state
    if relay.active_low:
        value = not state

    GPIO.setup(relay.pin, GPIO.OUT, initial=value)


@router.post('/relay/{pin}/off', status_code=204)
async def turn_off_relay(pin: int):
    """
    Attempts to turn off the specified relay. It takes in account whether the relay is active low or not.
    :param pin: GPIO pin used to control the relay
    :return: 204 if successful. 404 if a relay connected to that pin was not found.
    """
    relay = await get_relay(pin)
    if relay is None:
        raise HTTPException(**__not_found_error)
    else:
        await toggle_relay(relay, False)
        return Response(status_code=204)


@router.post('/relay/{pin}/on', status_code=204)
async def turn_on_relay(pin: int):
    """
        Attempts to turn on the specified relay. It takes in account whether the relay is active low or not
        :param pin: GPIO pin used to control the relay
        :return: 204 if successful. 404 if a relay connected to that pin was not found.
        """
    relay = await get_relay(pin)
    if relay is None:
        raise HTTPException(**__not_found_error)
    else:
        await toggle_relay(relay, True)
        return Response(status_code=204)


@router.get('/relays', status_code=200, response_model=List[RelayStateModel])
async def get_relays():
    """
    Lists all existing relays.
    :return: A list with all existing relays.
    """
    values = []
    async with pool.pool.acquire() as connection:
        async with connection.transaction():
            async for relay in connection.cursor('SELECT pin, name, active_low FROM relays'):
                state = GPIO.input(relay['pin'])
                values.append(RelayStateModel(**relay, on=state ^ relay['active_low']))

        return values


@router.post('/relay', status_code=200, response_model=RelayModel)
async def create_relay(relay: RelayModel):
    """
    Creates a new relay. Once created the relay can be turned off or on.
    :param relay: Relay to be created.
    :return: Created relay as read from the database.
    """
    async with pool.pool.acquire() as connection:
        stmt = await connection.prepare('INSERT INTO relays (pin, name, active_low) VALUES ($1, $2, $3)')
        try:
            await stmt.fetchval(relay.pin, relay.name, relay.active_low)
        except UniqueViolationError as ex:
            raise HTTPException(status_code=400, detail='A relay controlled by that pin already exists.')

    return await get_relay(relay.pin)


@router.put('/relay/{pin}', status_code=200, response_model=RelayModel)
async def update_relay(pin: int, relay: RelayModel):
    """
    Updates an existing relay.
    :param pin: Pin that controls the relay to be updated.
    :param relay: Data that will replace the existing relay.
    :return: Updated relay as read from the database.
    """
    async with pool.pool.acquire() as connection:
        stmt = await connection.prepare('UPDATE relays SET pin = $1, name = $2, active_low = $3 WHERE pin = $4')
        await stmt.fetchval(relay.pin, relay.name, relay.active_low, pin)

    return await get_relay(relay.pin)


@router.delete('/relay/{pin}', status_code=204)
async def delete_relay(pin: int):
    """
    Deletes the specified relay.
    :param pin: Pin that controls the relay to be deleted.
    :return:
    """
    async with pool.pool.acquire() as connection:
        stmt = await connection.prepare('DELETE FROM relays WHERE pin = $1')
        await stmt.fetchval(pin)

        return Response(status_code=204)