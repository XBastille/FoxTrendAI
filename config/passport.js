const passport = require('passport')
const bcrypt = require('bcryptjs')
const mongoose = require('mongoose')
const LocalStrategy = require('passport-local')


const User = require('../models/Users')

module.exports = function (passport) {
    passport.use(
        new LocalStrategy({
            usernameField: 'email'
        }, async (email, password, done) => {
            try {
                const user = await User.findOne({ email: email })
                if (!user) {
                    return done(null, false, { message: "User is not registered" })
                }
                const ismatch = await bcrypt.compare(password, user.password)
                if (ismatch) {
                    return done(null, user)
                }
                else {
                    return done(null, false, { message: "Password doesnt matched" })
                }
            } catch (error) {
                console.log(error)
            }
        })
    )
    passport.serializeUser(function (user, done) {
        done(null, user.id);
    });

    passport.deserializeUser(async function (id, done) {
        try {
            const user = User.findById(id)
            done(null, user)
        } catch (error) {
            console.log(error)
        }
    });
}

