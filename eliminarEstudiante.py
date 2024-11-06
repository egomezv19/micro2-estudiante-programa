import json
import boto3
from botocore.exceptions import ClientError
import os

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])  # Nombre de la tabla como variable de entorno

def lambda_handler(event, context):
    # Esta función será para el endpoint buscar (ya definida previamente)
    pass

def eliminar_estudiante(event, context):
    # Obtener los parámetros necesarios
    id_estudiante = event['queryStringParameters'].get('ID-Estudiante')
    dni = event['queryStringParameters'].get('DNI')
    
    if not id_estudiante or not dni:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Debe proporcionar ID-Estudiante y DNI para eliminar el estudiante'})
        }
    
    try:
        # Eliminar el item usando ambas claves
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