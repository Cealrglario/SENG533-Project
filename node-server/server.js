const http = require('http');

// Create an HTTP server that responds with a message to an incoming request
http.CreateServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/html'}); // indicate that response header includes html
    res.end('<h1>Hello from Node</h1>'); // actual response content
}).listen(3000); // listen on port 3000