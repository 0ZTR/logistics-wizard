"""
Handle all actions on the shipment resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the shipment
object and should just call into the service layer to act upon a shipment resource.
"""
import requests
import json
from server.config import Config
from server.exceptions import (ResourceDoesNotExistException)
from server.exceptions import (APIException,
                               AuthenticationException,
                               UnprocessableEntityException)

###########################
#         Utilities       #
###########################


def shipment_to_dict(shipment):
    """
    Convert an instance of the Shipment model to a dict.

    :param shipment:  An instance of the Shipment model.
    :return:      A dict representing the shipment.
    """
    return {
        'id': shipment.id,
        'status': shipment.status,
        'createdAt': shipment.createdAt,
        'updatedAt': shipment.updatedAt,
        'deliveredAt': shipment.deliveredAt,
        'estimatedTimeOfArrival': shipment.estimatedTimeOfArrival,
        'currentLocation': shipment.currentLocation,
        'fromId': shipment.fromId,
        'toId': shipment.toId
    }


###########################
#         Services        #
###########################

def get_shipments(token, retailer_id=None, status=None):
    """
    Get a list of shipments from the ERP system.

    :param token:       The ERP Loopback session token.
    :param status:      Status of the shipments to be retrieved.
    :param retailer_id: Retailer of the shipments to be retrieved.

    :return:         The list of existing shipments.
    """

    # Add status filter if present
    status_query = ""
    if status is not None:
        status_query += ("filter[where][status]=" + status)

    # Create and format request to ERP
    url = Config.ERP + "Shipments?" + status_query
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving shipments', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def get_shipment(token, shipment_id):
    """
    Get a shipment from the ERP system.

    :param token:       The ERP Loopback session token.
    :param shipment_id: The ID of the shipment to be retrieved.

    :return:         The retrieved shipment.
    """

    # Create and format request to ERP
    url = Config.ERP + "Shipments/" + shipment_id
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving shipment', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Shipment does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def delete_shipment(token, shipment_id):
    """
    Delete a shipment from the ERP system.

    :param token:       The ERP Loopback session token.
    :param shipment_id: The ID of the shipment to be deleted.
    """

    # Create and format request to ERP
    url = Config.ERP + "Shipments/" + shipment_id
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("DELETE", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error deleting shipment', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Shipment does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return


def update_shipment(token, shipment_id, shipment):
    """
    Update a shipment from the ERP system.

    :param token:       The ERP Loopback session token.
    :param shipment_id: The ID of the shipment to be retrieved.
    :param shipment:    The shipment object with values to update.

    :return:         The updated shipment.
    """

    # Create and format request to ERP
    url = Config.ERP + "Shipments/" + shipment_id
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("PUT", url, data=shipment, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error updating shipment', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    if response.status_code == 404:
        raise ResourceDoesNotExistException('Shipment does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text
