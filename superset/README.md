```
docker compose up -d
# after all UP
docker exec -it superset superset db upgrade
docker exec -it superset superset init
```

