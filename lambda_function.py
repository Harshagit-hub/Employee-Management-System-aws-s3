import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Employees")


def lambda_handler(event, context):

    # Function URL request
    if "requestContext" in event and "http" in event["requestContext"]:

        with open("index.html", "r", encoding="utf-8") as file:
            html = file.read()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": html
        }


    # API Gateway REST API request
    method = event.get("httpMethod")


    if method == "GET":

        response = table.scan()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Employee data fetched successfully",
                "employees": response.get("Items", [])
            })
        }


    elif method == "POST":

        data = json.loads(event.get("body", "{}"))

        table.put_item(Item=data)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Employee added successfully",
                "employee": data
            })
        }


    elif method == "PUT":

        data = json.loads(event.get("body", "{}"))

        table.put_item(Item=data)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Employee updated successfully",
                "employee": data
            })
        }


    elif method == "DELETE":

        data = json.loads(event.get("body", "{}"))

        table.delete_item(
            Key={
                "employeeId": data["employeeId"]
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Employee deleted successfully",
                "employee": data
            })
        }


    else:

        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Invalid HTTP method"
            })
        }
