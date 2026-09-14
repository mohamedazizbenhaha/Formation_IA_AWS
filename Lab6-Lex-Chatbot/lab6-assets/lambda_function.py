"""
Lab 6 - Amazon Lex V2 code hook for the MakeAppointment intent.

Replaces the Vocareum-provided Lambda code. Paste the whole file into the
Lambda console code editor and choose Deploy.

Runtime: Python 3.12 (any 3.9+ works)
Handler: lambda_function.lambda_handler

--------------------------------------------------------------------------
WHAT THIS DOES
--------------------------------------------------------------------------
Amazon Lex handles the conversation; this function handles the *business
rules* Lex cannot know about:

  * which appointment types exist, and how long each takes
  * what the surgery's opening hours are
  * which slots are already taken
  * what to say when the user asks for something impossible

Lex calls this function twice per turn cycle:

  invocationSource = "DialogCodeHook"        -> validate, ask for more
  invocationSource = "FulfillmentCodeHook"   -> actually book it

--------------------------------------------------------------------------
ONE DELIBERATE CHANGE FROM THE OFFICIAL LAB
--------------------------------------------------------------------------
The AWS sample uses random.randint() to invent availability, so the bot
gives different answers every time you test it. That is fine for a demo of
the API, but it makes a *classroom* demo unreproducible and impossible to
debug in front of people.

Here, availability is derived deterministically from the date itself
(see `get_availabilities`). The same date always yields the same slots,
so you can rehearse a demo and have it behave identically on the day.
--------------------------------------------------------------------------
"""

import datetime
import dateutil.parser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# ==========================================================================
# Business rules
# ==========================================================================

# Appointment type -> duration in minutes
APPOINTMENT_DURATIONS = {
    'cleaning': 30,
    'root canal': 60,
    'whitening': 30,
}

OPENING_HOUR = 10   # 10:00
CLOSING_HOUR = 17   # last appointment starts 16:30


# ==========================================================================
# Lex V2 response builders
#
# Every response has the same shape. The `dialogAction.type` tells Lex what
# to do next:
#   Delegate     - you decide, Lex (used when everything validates)
#   ElicitSlot   - ask the user for this specific slot
#   ConfirmIntent- ask the user to confirm before fulfilling
#   Close        - the conversation turn is finished
# ==========================================================================

def _response(session_attributes, dialog_action, intent_name,
              slots=None, state='InProgress', message=None):
    intent = {'name': intent_name, 'state': state}
    if slots is not None:
        intent['slots'] = slots

    response = {
        'sessionState': {
            'sessionAttributes': session_attributes or {},
            'dialogAction': dialog_action,
            'intent': intent,
        }
    }
    if message:
        response['messages'] = [{'contentType': 'PlainText', 'content': message}]
    return response


def delegate(session_attributes, intent_name, slots):
    """Hand control back to Lex to work out the next step itself."""
    return _response(session_attributes, {'type': 'Delegate'},
                     intent_name, slots)


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """Ask the user to (re)supply one particular slot."""
    return _response(session_attributes,
                     {'type': 'ElicitSlot', 'slotToElicit': slot_to_elicit},
                     intent_name, slots, message=message)


def confirm_intent(session_attributes, intent_name, slots, message):
    """Ask the user to confirm before we book."""
    return _response(session_attributes, {'type': 'ConfirmIntent'},
                     intent_name, slots, message=message)


def close(session_attributes, intent_name, state, message):
    """End the turn. state is 'Fulfilled' or 'Failed'."""
    return _response(session_attributes, {'type': 'Close'},
                     intent_name, state=state, message=message)


# ==========================================================================
# Slot helpers
#
# Lex V2 nests slot values:
#   slots['Time'] = {'value': {'interpretedValue': '10:00', ...}}
# and an unfilled slot is None, so every read needs guarding.
# ==========================================================================

def get_slot(slots, name):
    """Return the interpreted value of a slot, or None if not filled."""
    slot = (slots or {}).get(name)
    if not slot or not slot.get('value'):
        return None
    value = slot['value']
    return value.get('interpretedValue') or value.get('originalValue')


def set_slot(slots, name, value):
    """Write a normalised value back into a slot."""
    slots[name] = {
        'value': {
            'originalValue': value,
            'interpretedValue': value,
            'resolvedValues': [value],
        }
    }
    return slots


def validation_error(slot_name, message):
    return {'isValid': False, 'violatedSlot': slot_name, 'message': message}


# ==========================================================================
# Availability
# ==========================================================================

def get_duration(appointment_type):
    """Minutes for an appointment type, or None if unrecognised."""
    if not appointment_type:
        return None
    return APPOINTMENT_DURATIONS.get(appointment_type.lower())


def increment_time_by_thirty_mins(time_str):
    hour, minute = map(int, time_str.split(':'))
    return f'{hour + 1:02d}:00' if minute == 30 else f'{hour:02d}:30'


def get_availabilities(date_str):
    """
    Return the list of free 30-minute start times for a date.

    Deterministic: the same date always produces the same availability,
    which makes demos and debugging reproducible. A real implementation
    would query a booking database here.
    """
    parsed = dateutil.parser.parse(date_str).date()
    day_of_week = parsed.weekday()          # Monday = 0, Sunday = 6

    if day_of_week == 6:                    # closed Sundays
        return []

    # Every possible half-hour slot in the working day
    all_slots = []
    for hour in range(OPENING_HOUR, CLOSING_HOUR):
        all_slots.append(f'{hour:02d}:00')
        all_slots.append(f'{hour:02d}:30')

    # Deterministically "book out" some slots based on the date, so
    # different dates look different but any given date is stable.
    seed = parsed.toordinal()
    if day_of_week == 5:                    # Saturday: mornings only
        return [s for s in all_slots if int(s.split(':')[0]) < 13]

    return [s for i, s in enumerate(all_slots) if (i + seed) % 3 != 0]


def is_available(time_str, duration, availabilities):
    """Does this start time fit, given the appointment's duration?"""
    if duration == 30:
        return time_str in availabilities
    if duration == 60:
        second_half = increment_time_by_thirty_mins(time_str)
        return time_str in availabilities and second_half in availabilities
    raise ValueError(f'Unsupported duration: {duration}')


def get_availabilities_for_duration(duration, availabilities):
    """Filter the free slots down to those long enough for this booking."""
    if duration == 30:
        return list(availabilities)

    result = []
    for start in availabilities:
        if increment_time_by_thirty_mins(start) in availabilities:
            result.append(start)
    return result


def build_time_output(time_str):
    """Render 14:30 as '2:30 p.m.' for a friendlier message."""
    hour, minute = map(int, time_str.split(':'))
    suffix = 'a.m.' if hour < 12 else 'p.m.'
    display_hour = hour if 1 <= hour <= 12 else abs(hour - 12)
    return f'{display_hour}:{minute:02d} {suffix}'


def build_available_time_string(availabilities):
    """Turn a list of times into a readable sentence fragment."""
    if not availabilities:
        return 'no times'
    if len(availabilities) == 1:
        return f'{build_time_output(availabilities[0])}'
    shown = availabilities[:3]
    parts = [build_time_output(t) for t in shown]
    text = ', '.join(parts[:-1]) + f' or {parts[-1]}'
    if len(availabilities) > 3:
        text += ' (among others)'
    return text


# ==========================================================================
# Validation
# ==========================================================================

def validate_appointment(slots):
    appointment_type = get_slot(slots, 'AppointmentType')
    date_str = get_slot(slots, 'Date')
    time_str = get_slot(slots, 'Time')

    # ---- appointment type -------------------------------------------------
    if appointment_type and get_duration(appointment_type) is None:
        return validation_error(
            'AppointmentType',
            'I can book a cleaning, a root canal, or a whitening. '
            'Which would you like?')

    # ---- date -------------------------------------------------------------
    if date_str:
        try:
            appointment_date = dateutil.parser.parse(date_str).date()
        except (ValueError, OverflowError):
            return validation_error(
                'Date', 'I did not understand that date. '
                        'What day would you like to come in?')

        if appointment_date < datetime.date.today():
            return validation_error(
                'Date', 'Appointments cannot be booked in the past. '
                        'What day works for you?')

        if appointment_date.weekday() == 6:
            return validation_error(
                'Date', 'The surgery is closed on Sundays. '
                        'Which other day suits you?')

    # ---- time -------------------------------------------------------------
    if time_str:
        if ':' not in time_str:
            return validation_error(
                'Time', 'Please give a time like 10:30 or 2:00 p.m.')

        try:
            hour, minute = map(int, time_str.split(':')[:2])
        except ValueError:
            return validation_error(
                'Time', 'Please give a time like 10:30 or 2:00 p.m.')

        if hour < OPENING_HOUR or hour >= CLOSING_HOUR:
            return validation_error(
                'Time',
                f'Our hours are {OPENING_HOUR}:00 a.m. to '
                f'{CLOSING_HOUR - 12}:00 p.m. What time works for you?')

        if minute not in (0, 30):
            return validation_error(
                'Time', 'We book on the hour and half hour. '
                        'What time would you like?')

    # ---- availability (needs type + date + time) --------------------------
    if appointment_type and date_str and time_str:
        duration = get_duration(appointment_type)
        availabilities = get_availabilities(date_str)
        suitable = get_availabilities_for_duration(duration, availabilities)

        if not suitable:
            return validation_error(
                'Date',
                'We have nothing long enough that day. '
                'Could you try another date?')

        normalised = f'{int(time_str.split(":")[0]):02d}:{int(time_str.split(":")[1]):02d}'
        if not is_available(normalised, duration, availabilities):
            return validation_error(
                'Time',
                f'{build_time_output(normalised)} is not free. '
                f'We have {build_available_time_string(suitable)}. '
                'Which would you prefer?')

    return {'isValid': True}


# ==========================================================================
# Handler
# ==========================================================================

def lambda_handler(event, context):
    logger.info('Lex event: %s', event)

    session_state = event.get('sessionState', {})
    intent = session_state.get('intent', {})
    intent_name = intent.get('name', 'MakeAppointment')
    slots = intent.get('slots') or {}
    session_attributes = session_state.get('sessionAttributes') or {}
    source = event.get('invocationSource')
    confirmation = intent.get('confirmationState', 'None')

    # ---------- DialogCodeHook: validate as the user fills slots ----------
    if source == 'DialogCodeHook':

        # User said "no" at the confirmation prompt - start the slot over.
        if confirmation == 'Denied':
            return elicit_slot(
                session_attributes, intent_name, {}, 'AppointmentType',
                'No problem. What type of appointment would you like?')

        result = validate_appointment(slots)

        if not result['isValid']:
            # Clear the offending slot so Lex asks for it again
            slots[result['violatedSlot']] = None
            return elicit_slot(session_attributes, intent_name, slots,
                               result['violatedSlot'], result['message'])

        # Helpful nudge: once we know the type and date, offer times
        appointment_type = get_slot(slots, 'AppointmentType')
        date_str = get_slot(slots, 'Date')
        time_str = get_slot(slots, 'Time')

        if appointment_type and date_str and not time_str:
            duration = get_duration(appointment_type)
            suitable = get_availabilities_for_duration(
                duration, get_availabilities(date_str))
            if not suitable:
                slots['Date'] = None
                return elicit_slot(
                    session_attributes, intent_name, slots, 'Date',
                    'We have no openings that day. What other date suits you?')
            return elicit_slot(
                session_attributes, intent_name, slots, 'Time',
                f'We have {build_available_time_string(suitable)} available. '
                'What time would you like?')

        return delegate(session_attributes, intent_name, slots)

    # ---------- FulfillmentCodeHook: actually book it ----------------------
    if source == 'FulfillmentCodeHook':
        appointment_type = get_slot(slots, 'AppointmentType')
        date_str = get_slot(slots, 'Date')
        time_str = get_slot(slots, 'Time')

        # A real system would write to a booking database here.
        logger.info('BOOKING: %s on %s at %s',
                    appointment_type, date_str, time_str)

        return close(
            session_attributes, intent_name, 'Fulfilled',
            f'Booked. Your {appointment_type} is on {date_str} '
            f'at {build_time_output(time_str)} - see you then.')

    # ---------- Anything else ---------------------------------------------
    logger.warning('Unexpected invocationSource: %s', source)
    return close(session_attributes, intent_name, 'Failed',
                 'Sorry, something went wrong booking that.')
