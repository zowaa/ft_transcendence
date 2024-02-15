const express = require('express');
const path = require('path');
const app = express();

app.use('/Frontend', express.static(path.join(__dirname, 'Frontend')));

app.get('/*', (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(process.env.PORT || 3000, () => {
  console.log(`Server is running on port ${process.env.PORT || 3000}`);
});
