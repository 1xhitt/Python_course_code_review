
# WORL IN PROGRESS

# cont_info=$(sudo docker volume inspect crp-db)

# make sure volume is a thing
# if [[ -z "${cont_info[@]}" ]]
# then
#     sudo docker volume create crp-db
#     sudo docker run -v crp-db:/data --name helper busybox true
#     sudo docker cp database helper:/data
#     sudo docker rm helper
# fi
sudo docker-compose build
sudo docker-compose up


