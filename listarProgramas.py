import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Acceder al body directamente (asumiendo que ya es un diccionario JSON)
    body = json.loads(event['body'])
    id_programa = body['ID_Programa']
    
    # Inicialización de DynamoDB y tabla
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('programa_t')
    
    # Realizar la consulta para obtener detalles del programa específico
    try:
        response = table.query(
            KeyConditionExpression=Key('ID_Programa').eq(id_programa)
        )
        
        # Salida (json)
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])  # Devuelve todos los detalles del programa
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error en la consulta: {str(e)}')
        }
