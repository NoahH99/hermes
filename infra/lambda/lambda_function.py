import json
import boto3
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def lambda_handler(event, context):
    ecs_client = boto3.client('ecs')

    service_name = event.get("Service", "hermes-service")
    cluster_name = event.get("Cluster", "hermes-cluster-prod")
    desired_count = event.get("DesiredCount")

    if desired_count is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "DesiredCount must be provided in the event."
            })
        }

    try:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=desired_count
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Service '{service_name}' updated successfully to DesiredCount={desired_count}.",
                "response": response
            }, cls=DateTimeEncoder)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Failed to update service '{service_name}'.",
                "error": str(e)
            })
        }
