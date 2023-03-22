const http = require('http');

const fs = require('fs');

const path = require('path');



const server = http.createServer((req, res) => {

  if (req.url === '/') {

    // Serve the index.html file

    const filePath = path.join(__dirname, 'index.html'); // create an absolute path

    fs.readFile(filePath, (err, data) => {

      if (err) {

        res.writeHead(500, {'Content-Type': 'text/plain'});

        res.write('Error loading index.html');

        res.end();

        return;

      }

      res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});

      res.write(data);

      res.end();

    });

  } else if (req.url === '/index.js') {

    // Serve the index.js file

    const filePath = path.join(__dirname, 'index.js'); // create an absolute path

    fs.readFile(filePath, (err, data) => {

      if (err) {

        res.writeHead(500, {'Content-Type': 'text/plain'});

        res.write('Error loading index.js');

        res.end();

        return;

      }

      res.writeHead(200, {'Content-Type': 'application/javascript; charset=utf-8'});

      res.write(data);

      res.end();

    });

  } else {

    // Return a 404 error for all other requests

    res.writeHead(404, {'Content-Type': 'text/plain'});

    res.write('Page not found');

    res.end();

  }

});



server.listen(3000, () => {

  console.log('Server running on port 3000');

});