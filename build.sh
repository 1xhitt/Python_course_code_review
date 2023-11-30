
# WORL IN PROGRESS

# cont_info=$(sudo docker volume inspect crp-db)

# # make sure volume is a thing
# if [[ -z "${cont_info[@]}" ]]
# then
#     docker volume create crp-db
#     docker run -v crp-db:/data --name helper busybox true
#     docker cp database helper:/data
#     docker rm helper
# fi

