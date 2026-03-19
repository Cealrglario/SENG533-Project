# Import lightweight Alpine Linux version of Node.js
FROM node:20-alpine

# Set the container working directory
WORKDIR /usr/src/app

# Copy our server.js file into the docker container
COPY server.js .

# Tell Docker to listen on port 3000 
EXPOSE 3000

# Execute the server.js file with Node.js when the container is ran
CMD ["node", "server.js"]