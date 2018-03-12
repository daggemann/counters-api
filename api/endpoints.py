from functools import wraps

from flask import Blueprint, jsonify, request

from api.models import Counter

counters_blueprint = Blueprint('counters', '__name__')


def validate_counter(f):
    """
        Decorator that validates if a counter with a given id exists.
        If it exists it adds the counter as an argument to the decorated function.
        If not it returns with a 404.
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        id = kwargs['id']
        counter = Counter.get_by_id(id)
        if not counter:
            return jsonify({'status': 'error', 'reason': 'Resource not found.'}), 404
        return f(counter, *args, **kwargs)

    return decorated_function


def required_fields(fields):
    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = request.get_json()
            for field in fields:
                if field not in payload:
                    return jsonify({'status': 'error', 'reason': 'Invalid payload.'}), 400
            return f(*args, **kwargs)

        return wrapper

    return actual_decorator


@counters_blueprint.route('/counters', methods=['GET'])
def get_counters():
    """
        Return JSON representation of all existing counters.

    :return: JSON representation of all existing counters (status code 200)
    """
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>/increment', methods=['POST'])
@validate_counter
def increment_counter(counter, id):
    """
        Increment the count for a counter. If id is not a valid id the validate_counter will return 404.

    :param counter: provided by validate_counter decorator
    :param id: provided by route decorator
    :return: JSON representation of all existing counters (status code 200)
    """
    counter.count += 1
    counter.commit()

    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>/decrement', methods=['POST'])
@validate_counter
def decrement_counter(counter, id):
    """
        Decrement the count for a counter. If id is not a valid id the validate_counter will return 404.

    :param counter: provided by validate_counter decorator
    :param id: provided by route decorator
    :return: JSON representation of all existing counters (status code 200)
    """
    counter.count -= 1
    counter.commit()

    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>', methods=['DELETE'])
@validate_counter
def delete_counter(counter, id):
    """
        Delete a counter. If id is not a valid id the validate_counter will return 404.

    :param counter: provided by validate_counter decorator
    :param id: provided by route decorator
    :return: JSON representation of all existing counters (status code 200)
    """
    counter.delete_and_commit()

    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters', methods=['POST'])
@required_fields(['title'])
def add_counter():
    """
        Add a new counter with title as provided in payload. If title is not given in payload the decorator
        required_fields will return with 400.

        Empty title is not allowed.

    :return: JSON representation of all existing counters (status code 201)
    """
    title = request.get_json()['title']
    if len(title) == 0:
        return jsonify({'status': 'error', 'reason': 'Invalid payload.'}), 400

    counter = Counter(title)
    counter.add_and_commit()

    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 201
