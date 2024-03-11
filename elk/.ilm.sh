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

  # Associate ILM Policy with an Index Template
  curl -k -X PUT -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_template/containers_logs_template" -H 'Content-Type: application/json' -d '{
    "index_patterns": ["containers_logs*"],
    "settings": {
      "index": {
        "lifecycle": {
          "name": "containers_logs_policy",
          "rollover_alias": "containers_logs"
        }
      }
    }
  }'

  curl -k -X PUT -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "${ELASTICSEARCH_HOSTS}/_template/users_data_template" -H 'Content-Type: application/json' -d '{
    "index_patterns": ["users_data*"],
    "settings": {
      "index": {
        "lifecycle": {
          "name": "users_data_policy",
          "rollover_alias": "users_data"
        }
      }
    }
  }'
fi

# {"acknowledged":true}
# echo "ILM policy created successfully"