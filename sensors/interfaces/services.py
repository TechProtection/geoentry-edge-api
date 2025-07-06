"""Interface services for Sensors context."""
from flask import Blueprint, request, jsonify
from sensors.application.services import SensorApplicationService

sensor_api = Blueprint("sensor_api", __name__)
sensor_service = SensorApplicationService()


@sensor_api.route('/sensors/user/<user_id>', methods=['GET'])
def get_sensors_by_user(user_id):
    """Get all sensors for a user.
    ---
    tags:
      - Sensors
    parameters:
      - in: path
        name: user_id
        required: true
        type: string
        description: The ID of the user
      - in: query
        name: active_only
        type: boolean
        description: Filter only active sensors
      - in: query
        name: sensor_type
        type: string
        description: Filter by sensor type
        enum: [led_tv, smart_light, air_conditioner, coffee_maker]
    responses:
      200:
        description: List of sensors
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  sensor_type:
                    type: string
                  isActive:
                    type: boolean
                  user_id:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      400:
        description: Invalid request
      500:
        description: Internal server error
    """
    try:
        # Get query parameters
        active_only = request.args.get('active_only', '').lower() == 'true'
        sensor_type = request.args.get('sensor_type')
        
        # Get sensors based on filters
        if sensor_type:
            sensors = sensor_service.get_sensors_by_type(user_id, sensor_type)
        elif active_only:
            sensors = sensor_service.get_active_sensors_by_user(user_id)
        else:
            sensors = sensor_service.get_sensors_by_user(user_id)
        
        return jsonify({
            'success': True,
            'data': [sensor.to_dict() for sensor in sensors],
            'count': len(sensors)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@sensor_api.route('/sensors/<sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    """Get sensor by ID.
    ---
    tags:
      - Sensors
    parameters:
      - in: path
        name: sensor_id
        required: true
        type: string
        description: The ID of the sensor
    responses:
      200:
        description: Sensor details
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                sensor_type:
                  type: string
                isActive:
                  type: boolean
                user_id:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      404:
        description: Sensor not found
      500:
        description: Internal server error
    """
    try:
        sensor = sensor_service.get_sensor(sensor_id)
        
        if not sensor:
            return jsonify({
                'success': False,
                'error': 'Sensor not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': sensor.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@sensor_api.route('/sensors/<sensor_id>/status', methods=['PATCH'])
def update_sensor_status(sensor_id):
    """Update sensor status (activate/deactivate).
    ---
    tags:
      - Sensors
    parameters:
      - in: path
        name: sensor_id
        required: true
        type: string
        description: The ID of the sensor
      - in: body
        name: status_data
        required: true
        schema:
          type: object
          required:
            - isActive
          properties:
            isActive:
              type: boolean
              description: New status for the sensor
              example: true
    responses:
      200:
        description: Sensor status updated successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                sensor_type:
                  type: string
                isActive:
                  type: boolean
                user_id:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      400:
        description: Invalid request data
      404:
        description: Sensor not found
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        if 'isActive' not in data:
            return jsonify({
                'success': False,
                'error': 'isActive field is required'
            }), 400
        
        is_active = data['isActive']
        
        if not isinstance(is_active, bool):
            return jsonify({
                'success': False,
                'error': 'isActive must be a boolean value'
            }), 400
        
        # Update sensor status
        updated_sensor = sensor_service.update_sensor_status(sensor_id, is_active)
        
        action = "activated" if is_active else "deactivated"
        
        return jsonify({
            'success': True,
            'message': f'Sensor {action} successfully',
            'data': updated_sensor.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if 'not found' in str(e) else 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@sensor_api.route('/sensors/user/<user_id>/statistics', methods=['GET'])
def get_sensor_statistics(user_id):
    """Get sensor statistics for a user.
    ---
    tags:
      - Sensors
    parameters:
      - in: path
        name: user_id
        required: true
        type: string
        description: The ID of the user
    responses:
      200:
        description: Sensor statistics
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                total_sensors:
                  type: integer
                active_sensors:
                  type: integer
                inactive_sensors:
                  type: integer
                sensors_by_type:
                  type: object
      400:
        description: Invalid request
      500:
        description: Internal server error
    """
    try:
        statistics = sensor_service.get_sensor_statistics(user_id)
        
        return jsonify({
            'success': True,
            'data': statistics
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
