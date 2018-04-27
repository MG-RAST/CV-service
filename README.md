
# Install 

```bash
git clone git@github.com:MG-RAST/CV-service.git
cd CV-Service
docker-compose up
```


# Example API calls


List of all terms
```text
curl http://localhost:5001/api/term
```

Get object by name
```text
curl http://localhost:5001/api/term/BIS
```

Get object by 
```text
curl http://localhost:5001/api/id/1
```
 
Create new object with synonyms
```text
curl -X POST -H 'Content-Type: application/json' 'http://localhost:5001/api/term' -d '{"name": "example_term", "synonyms": ["synonym_a", "synonym_b"]}'
```