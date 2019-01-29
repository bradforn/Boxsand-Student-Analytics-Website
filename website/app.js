var path = require('path');
var express = require('express');
var exphbs = require('express-handlebars');

var app = express();
var port = process.env.PORT || 3000;

// Use Handlebars as the view engine for the app.
app.engine('handlebars', exphbs({ defaultLayout: 'main' }))
app.set('view engine', 'handlebars');

// Serve static files from public/.
app.use(express.static(path.join(__dirname, 'public')));

/*
 * Route the root path ('/') to the index page.  Give Handlebars the
 * appropriate page title and data for all users to render.
 */
app.get('/', function (req, res) {
  res.render('main-page', {
    title: 'Welcome to My Website',

  });
});

app.get('/about', function (req, res) {
  res.render('about-page', {
    title: 'About Me',

  });
});


app.get('/list-users', function (req, res) {
  res.render('list-users', {
    title: 'Users',

  });
});






// Return a 404 and render the 404 page for any other route.
app.get('*', function (req, res) {
  res.render('404-page', {
     title: 'Page Not Found!',
     layout: '404'
  });

});

// Listen on the specified port.
app.listen(port, function () {
  console.log("== Listening on port", port);
});
