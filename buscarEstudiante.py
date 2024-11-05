import json
import boto3

def lambda_handler(event, context):
    # Acceder al body directamente (asumiendo que ya es un diccionario)
    body = json.loads(event['body'])
    id_estudiante = body['id_estudiante']
    dni = body['dni']
    
    # Inicialización de DynamoDB y tabla
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('estudiante_t')
    
    # Realizar la consulta para obtener detalles del estudiante específico usando id_estudiante y dni
    response = table.get_item(
        Key={
            'id_estudiante': id_estudiante,
            'dni': dni
        }
    )
    
    # Verificar si el estudiante fue encontrado
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])  # Devuelve todos los detalles del estudiante
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Estudiante no encontrado'})
        }
