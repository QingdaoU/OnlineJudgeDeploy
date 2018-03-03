#!/bin/sh
docker exec oj-postgres psql -U onlinejudge -d onlinejudge -t -A -c "select array_to_json(array_agg(row_to_json(temp))) from (select distinct on (username) id, create_time, username, language, code from submission order by username, create_time desc) as temp;" -o /tmp/res.txt
docker cp oj-postgres:/tmp/res.txt .
mkdir -p codes && rm -rf codes/*
python3 -c "import json,os,base64;ext={'C':'c','C++':'cpp','Java':'java','Python2':'py','Python3':'py'};s=json.load(open('res.txt'));[open(os.path.join('codes','{}-{}.{}'.format(r['id'],base64.urlsafe_b64encode(r['username'].encode()).decode(),ext[r['language']])),'w').write(r['code']) for r in s];"
tar zcvf codes.tgz codes
