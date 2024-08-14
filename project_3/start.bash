if [ ! "$DB_HOST" ] && [ ! "$(docker ps -a | grep postgres)" ]; then
  # docker run --name postgres -e POSTGRES_PASSWORD=todo -d postgres
  docker run --name postgres -e POSTGRES_USER=todo -e POSTGRES_PASSWORD=todo -e POSTGRES_DB=todos -p 5432:5432 -d postgres
fi

(cd ../; uvicorn project_3.main:app --reload)