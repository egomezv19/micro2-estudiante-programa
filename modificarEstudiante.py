import json
import boto3
from botocore.exceptions import ClientError
import os

def modificar_estudiante(event, context):
    # Obtener los datos necesarios del cuerpo de la solicitud
    body = json.loads(event['body'])
    id_estudiante = body.get('ID-Estudiante')
    dni = body.get('DNI')
    
    # Asegurarse de que las claves principales están presentes
    if not id_estudiante or not dni:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Debe proporcionar ID-Estudiante y DNI para modificar el estudiante'})
        }
    
    # Crear un diccionario para los atributos a actualizar
    update_expression = "SET "
    expression_attribute_values = {}
    for key, value in body.items():
        if key not in ["ID-Estudiante", "DNI"]:  # No actualizar las claves primarias
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value

    # Eliminar la última coma y espacio
    update_expression = update_expression.rstrip(", ")

    try:
        # Actualizar el item en DynamoDB
        response = table.update_item(
            Key={
                'ID-Estudiante': id_estudiante,
                'DNI': dni
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Estudiante actualizado correctamente', 'updatedItem': response['Attributes']})
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al actualizar el estudiante', 'details': str(e)})
        }