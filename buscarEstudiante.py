import json
import boto3
from botocore.exceptions import ClientError
import os

def lambda_handler(event, context):
    # Inicio - Proteger el Lambda
    try:
        token = event['headers']['Authorization']  # Obtener el token de autenticación desde el header
    except KeyError:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Falta el token de autenticación'})
        }
    
    # Invocar la función Lambda de validación de token
    lambda_client = boto3.client('lambda')
    payload_string = json.dumps({"token": token})
    
    invoke_response = lambda_client.invoke(
        FunctionName="ValidarTokenAcceso",  # Nombre de la función Lambda para validar el token
        InvocationType="RequestResponse",
        Payload=payload_string
    )
    
    response = json.loads(invoke_response['Payload'].read())
    
    # Verificar el resultado de la validación del token
    if response.get('statusCode') == 403:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Acceso No Autorizado - Token no válido'})
        }
    # Fin - Proteger el Lambda

    # Acceder al body directamente como un diccionario
    body = event['body']
    id_estudiante = body.get('ID-Estudiante')
    dni = body.get('DNI')
    
    # Verificar que ambos parámetros estén presentes
    if not id_estudiante or not dni:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Debe proporcionar ID-Estudiante y DNI'})
        }
    
    # Inicialización de DynamoDB y tabla
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Estudiante')  # Usar el nombre correcto de la tabla: Estudiante
    
    try:
        # Realizar la consulta en DynamoDB usando ID-Estudiante y DNI
        response = table.get_item(
            Key={
                'ID-Estudiante': id_estudiante,
                'DNI': dni
            }
        )
        
        # Verificar si el estudiante fue encontrado
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Estudiante no encontrado'})
            }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al acceder a DynamoDB', 'details': str(e)})
        }
