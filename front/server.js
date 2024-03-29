// const express = require('express');
// const path = require('path');
// const app = express();

// app.use('/Frontend', express.static(path.join(__dirname, 'Frontend')));

// app.get('/*', (req, res) => {
//   res.sendFile(path.join(__dirname, "index.html"));
// });

// app.listen(process.env.PORT || 8080, () => {
//   console.log(`Server is running on port ${process.env.PORT || 8080}`);
// });


// https server && logs with morgan //

const https = require('https');
const fs = require('fs');
const express = require('express');
const path = require('path');
const morgan = require('morgan');
const app = express();

// Define paths to SSL certificate and key files
const sslOptions = {
    key: fs.readFileSync('/home/node/app/certs/key.pem'),
    cert: fs.readFileSync('/home/node/app/certs/cert.pem')
};

// Use morgan middleware for logging to stdout
app.use(morgan('combined'));

// Serve static files from the 'Frontend' directory
app.use('/Frontend', express.static(path.join(__dirname, 'Frontend')));

// Route all other requests to serve the index.html file
app.get('/*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Create an HTTPS server
const server = https.createServer(sslOptions, app);

// Start the server
const PORT = process.env.PORT || 443; // Default to port 443 for HTTPS
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

