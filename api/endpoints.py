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

@counters_blueprint.route('/counters', methods=['GET'])
def get_counters():
    """
        Return JSON representation of all existing counters.
    """
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>/increment', methods=['POST'])
@validate_counter
def increment_counter(counter, id):
    counter.count += 1
    counter.commit()

    # TODO: The below action should be extracted into a funtion because it is used in every request
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>/decrement', methods=['POST'])
@validate_counter
def decrement_counter(counter, id):
    counter.count -= 1
    counter.commit()

    # TODO: The below action should be extracted into a funtion because it is used in every request
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>', methods=['DELETE'])
@validate_counter
def delete_counter(counter, id):
    counter.delete_and_commit()

    # TODO: The below action should be extracted into a funtion because it is used in every request
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters', methods=['POST'])
def add_counter():
    # TODO: Needs validation, possibly a decorator @required(('title', 'str'))
    data = request.get_json()
    new_counter = Counter(data['title'])

    new_counter.add_and_commit()

    # TODO: The below action should be extracted into a funtion because it is used in every request
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 201
