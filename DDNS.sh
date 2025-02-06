HOSTED_ZONE_ID="Z06156031UB19F5X1RSVS"
DOMAIN_NAME="rag-query.com"
NEW_IP=$(curl -s http://checkip.amazonaws.com)

aws route53 change-resource-record-sets --hosted-zone-id $HOSTED_ZONE_ID --change-batch "
{
    \"Changes\": [
        {
            \"Action\": \"UPSERT\",
            \"ResourceRecordSet\": {
                \"Name\": \"$DOMAIN_NAME\",
                \"Type\": \"A\",
                \"TTL\": 300,
                \"ResourceRecords\": [{ \"Value\": \"$NEW_IP\" }]
            }
        }
    ]
}"