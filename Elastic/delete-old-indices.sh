# Finds and deletes indices older than an specific month.

#!/bin/bash
for i in $(curl -X GET "https://xxx:9200/_cat/indices?v&h=index" --insecure -u elastic:XXXX | grep -E '*2025\.0[1-9]\..*')
do
 echo $i
 curl -X DELETE "https:/xxx:9200/$i" --insecure -u elastic:XXXX
done
