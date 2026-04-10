const http = require('http');

// Function to test dynamic web server requests
function calculateFibonacci(n) {
    if (n <= 1) return n;
    return calculateFibonacci(n - 1) + calculateFibonacci (n - 2);
}
    
// Create an HTTP server that responds with a message to an incoming request
http.createServer((req, res) => {
    // ROUTE FOR STATIC WEB SERVER REQUEST
    if (req.url === '/' || req.url === '/index.html') {
        // HTTP code, header contents
        res.writeHead(200, {'Content-Type': 'text/html'}); // reply with 200 OK and indicate that response header includes html
        res.end('<h1>Hello from Node</h1>'); // actual response content
    }

    // ROUTE FOR DYNAMIC WEB SERVER REQUEST
    else if (req.url === '/fibonacci') {
        const result = calculateFibonacci(15);
        res.writeHead(200, {'Content-Type': 'text/plain'}); // reply with 200 OK and indicate that response header includes plain text
        res.end(`Fibonacci 15: ${result}`);
    }

    else {
        res.writeHead(404, {'Content-Type': 'text/plain'});
        res.end('404 Not Found');   
    }
}).listen(3000); // listen to port 3000 inside the container