const exp = require('constants');
const express = require('express')
const path = require('path')
const passport = require('passport')
const session = require('express-session');
const { default: mongoose } = require('mongoose');

const app = express()
const port = 3000;

const db = require('./config/key').MongoURI

mongoose.connect(db, { useNewUrlParser: true })
    .then(() => {
        console.log("Mongodb connected")
    })
    .catch(err => console.log(err))

app.use(session({
    secret: 'secret',
    saveUninitialized: true,
    resave:true
}));

app.use(passport.initialize());
app.use(passport.session());

//template engine
app.set('view engine', 'hbs');

app.use("/public", express.static(path.join(__dirname, 'public')));

app.use(express.json());

// middleware
app.use(express.urlencoded({ extended: false }))



app.use('/', require('./route/index'))
app.use('/user', require('./route/user'))

app.listen(port, () => {
    console.log("app is listening to the port 3000")
})