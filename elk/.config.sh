#!/bin/sh

ILM_POLICY_BODY='
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "5GB",
            "max_age": "1m"
          }
        }
      },
      "delete": {
        "min_age": "0ms",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
'

# ILM Policy Configuration
if [ $(curl -s -o /dev/null -w "%{http_code}" -k -X GET -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_ilm/policy/${ILM_POLICY_NAME1}" -H 'Content-Type: application/json') -ne 200 ] &&
   [ $(curl -s -o /dev/null -w "%{http_code}" -k -X GET -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_ilm/policy/${ILM_POLICY_NAME2}" -H 'Content-Type: application/json') -ne 200 ]
then
  # Create ILM Policy
  curl -k -X PUT -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_ilm/policy/${ILM_POLICY_NAME1}" -H 'Content-Type: application/json' -d "${ILM_POLICY_BODY}"

  curl -k -X PUT -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_ilm/policy/${ILM_POLICY_NAME2}" -H 'Content-Type: application/json' -d "${ILM_POLICY_BODY}"

  curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "https://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form file=@/usr/share/kibana/config/users_stats_dashboard.ndjson
  curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "https://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form file=@/usr/share/kibana/config/app_logs_dashboard.ndjson

  curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_security/role/viewer_role" -H 'Content-Type: application/json' -d '{
    "cluster": ["monitor"],
    "indices": [
      {                                              
        "names": ["containers_logs*", "users_data*"],
        "privileges": ["view_index_metadata", "manage", "read", "all"]
      }
    ]
  }'

  curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_security/user/${VIEWER_USER}" -H 'Content-Type: application/json' -d "{
    \"password\" : \"${VIEWER_PASSWORD}\",
    \"roles\" : [ \"viewer_role\", \"kibana_user\" ]
  }"

  curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_security/user/${MONITOR_USER}" -H 'Content-Type: application/json' -d "{
    \"password\" : \"${MONITOR_PASSWORD}\",
    \"roles\" : [ \"kibana_user\", \"monitoring_user\" ]
  }"
  
fi

# {"acknowledged":true}
# echo "ILM policy created successfully"