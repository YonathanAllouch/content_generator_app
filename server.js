
const express = require('express');
const app = express();

app.use(express.json());  // Middleware to parse JSON bodies

app.post('/generate_post', (req, res) => {
    // Example response to POST request
    res.json({ message: 'Post received', data: req.body });
});

const server = app.listen(5000, '0.0.0.0', function() {
    console.log('Server listening on port 5000');
});
