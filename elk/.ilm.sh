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
    },
    "mappings": {
    "_doc": {
      "properties": {
        "container": {
          "properties": {
            "name": {
              "type": "keyword"
            },
            "id": {
              "type": "keyword"
            }
          }
        },
        "image": {
          "properties": {
            "name": {
              "type": "keyword"
            },
            "id": {
              "type": "keyword"
            }
          }
        },
        "status": {
          "type": "keyword"
        },
        "message": {
          "type": "text"
        }
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
    "mappings": {
    "_doc": {
      "properties": {
        "id": {
          "type": "keyword"
        },
        "email": {
          "type": "keyword"
        },
        "username": {
          "type": "keyword"
        },
        "display_name": {
          "type": "keyword"
        },
        "date_joined": {
          "type": "date"
        },
        "last_login": {
          "type": "date"
        },
        "avatar": {
          "type": "keyword"
        },
        "friends": {
          "type": "keyword"
        },
        "nb_wins": {
          "type": "integer"
        },
        "nb_losses": {
          "type": "integer"
        },
        "nb_plays": {
          "type": "integer"
        },
        "status": {
          "type": "keyword"
        },
        "is_active": {
          "type": "boolean"
        },
        "is_42_user": {
          "type": "boolean"
        }
      }
    }
  }
  }'

  # while ! nc -z https://localhost 5601; do
  #   echo "Waiting for kibana to be ready..."
  #   sleep 1
  # done

  curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "https://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form file=@/usr/share/kibana/config/users_stats_final_dashboard.ndjson
  curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "https://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form file=@/usr/share/kibana/config/containers_logs_final_dashboard.ndjson
  # curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "https://localhost:5601/api/saved_objects/_import?overwrite=true" -H "kbn-xsrf: true" --form file=@/usr/share/kibana/config/export.ndjson
  # curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "https://localhost:5601/api/kibana/dashboards/import" -H 'Content-Type: application/json' -d @/usr/share/kibana/config/containers_logs_final_dashboard.ndjson
  # curl -k -X POST -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" "https://localhost:5601/api/kibana/dashboards/import" -H 'Content-Type: application/json' -d @/usr/share/kibana/config/users_stats_final_dashboard.ndjson
fi

# {"acknowledged":true}
# echo "ILM policy created successfully"