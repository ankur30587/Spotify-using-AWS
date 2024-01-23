aws apigateway create-rest-api --name MusicApplication --region us-east-1
aws apigateway get-resources --rest-api-id $API --region us-east-1
aws apigateway create-resource --rest-api-id $API --path-part MusicApplication --parent-id uepylo4pbj --region us-east-1
aws apigateway put-method --rest-api-id $API --resource-id $RESOURCE --http-method POST --authorization-type NONE --region us-east-1
aws apigateway put-integration --rest-api-id $API --resource-id $RESOURCE --http-method POST --type AWS --integration-http-method POST --uri arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/arn:aws:lambda:$REGION:$ACCOUNT:function:all_songs/invocations --region us-east-1
aws apigateway put-method-response --rest-api-id $API --resource-id $RESOURCE --http-method POST --status-code 200 --response-models application/json=Empty --region us-east-1
aws apigateway put-integration-response --rest-api-id $API --resource-id $RESOURCE --http-method POST --status-code 200 --response-templates application/json="" --region us-east-1
aws apigateway create-deployment --rest-api-id $API --stage-name prod --region us-east-1
aws lambda add-permission --function-name all_songs --statement-id apigateway-prod-2 --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT:$API/prod/POST/MusicApplication" --region us-east-1
aws apigateway test-invoke-method --rest-api-id $API --resource-id $RESOURCE --http-method POST --path-with-query-string "" --region us-east-1 --body file://all_songs.json
