const port = process.env.PORT || 3000;
const express = require("express");
const app = express();
app.set('view engine', 'ejs');

app.use('/public', express.static('public'));
app.use("/", require("./render"));
app.use("/images", require("./images"));

app.listen(port, () => console.log(`listening on :${port}!`));