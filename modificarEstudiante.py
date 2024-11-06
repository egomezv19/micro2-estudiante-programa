import json
import boto3
from botocore.exceptions import ClientError
import os

def modificar_estudiante(event, context):
    # Leer los datos desde el cuerpo de la solicitud
    body = json.loads(event['body'])
    id_estudiante = body.get('ID-Estudiante')
    dni = body.get('DNI')
    
    if not id_estudiante or not dni:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Debe proporcionar ID-Estudiante y DNI para modificar el estudiante'})
        }
    
    update_expression = "SET "
    expression_attribute_values = {}
    for key, value in body.items():
        if key not in ["ID-Estudiante", "DNI"]:
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value

    update_expression = update_expression.rstrip(", ")

    try:
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