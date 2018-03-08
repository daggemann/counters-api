from flask import Blueprint, jsonify, request

from api.models import Counter

counters_blueprint = Blueprint('counters', '__name__')


@counters_blueprint.route('/counters', methods=['GET'])
def get_counters():
    """
        Return JSON representation of all existing counters.
    """
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>/increment', methods=['POST'])
def increment_counter(id):
    # TODO: Should add a decorater that checks that id exists...
    counter = Counter.query.filter_by(id=id).first()
    counter.count += 1
    counter.commit()

    # TODO: The below action should be extracted into a funtion because it is used in every request
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>/decrement', methods=['POST'])
def decrement_counter(id):
    # TODO: Should add a decorater that checks that id exists...
    counter = Counter.query.filter_by(id=id).first()
    counter.count -= 1
    counter.commit()

    # TODO: The below action should be extracted into a funtion because it is used in every request
    counters = Counter.get_all()
    response_object = [counter.to_dict() for counter in counters]
    return jsonify(response_object), 200


@counters_blueprint.route('/counters/<id>', methods=['DELETE'])
def delete_counter(id):
    # TODO: Should add a decorater that checks that id exists...
    Counter.query.filter_by(id=id).delete()

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

