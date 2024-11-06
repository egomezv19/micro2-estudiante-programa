import json
import boto3
from botocore.exceptions import ClientError

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Estudiante')  # Reemplaza 'Estudiante' con el nombre exacto de tu tabla

def lambda_handler(event, context):
    # Obtener parámetros de búsqueda
    id_estudiante = event.get('ID-Estudiante')
    email = event.get('Email')
    
    try:
        if id_estudiante:
            # Búsqueda por ID-Estudiante (consulta principal)
            response = table.get_item(Key={'ID-Estudiante': id_estudiante})
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
        
        elif email:
            # Búsqueda por Email usando el índice global
            response = table.query(
                IndexName='EmailGSI',  # Nombre del índice global que creaste para Email
                KeyConditionExpression=boto3.dynamodb.conditions.Key('Email').eq(email)
            )
            if 'Items' in response and response['Items']:
                return {
                    'statusCode': 200,
                    'body': json.dumps(response['Items'])
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Estudiante no encontrado con ese Email'})
                }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Debe proporcionar ID-Estudiante o Email para buscar'})
            }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al acceder a DynamoDB', 'details': str(e)})
        }
