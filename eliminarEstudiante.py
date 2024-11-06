import json
import boto3
from botocore.exceptions import ClientError
import os

def eliminar_estudiante(event, context):
    # Leer los datos desde el cuerpo de la solicitud
    body = json.loads(event['body'])
    id_estudiante = body.get('ID-Estudiante')
    dni = body.get('DNI')
    
    if not id_estudiante or not dni:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Debe proporcionar ID-Estudiante y DNI para eliminar el estudiante'})
        }
    
    try:
        response = table.delete_item(
            Key={
                'ID-Estudiante': id_estudiante,
                'DNI': dni
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Estudiante eliminado correctamente'})
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al eliminar el estudiante', 'details': str(e)})
        }