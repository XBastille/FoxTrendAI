const express = require('express')
const bcrypt = require('bcryptjs')
const { spawn } = require('child_process');
const passport = require('passport')
const { promises } = require('dns');
const { resolve } = require('path');
const router = express.Router();

router.get('/login', (req, res) => {
  res.render("login")
})

router.get('/register', (req, res) => {
  res.render("register")
})

router.get('/forgot', (req, res) => {
  res.render("forgot")
})


const User = require('../models/Users');
require('../config/passport')(passport)

const runjava = (className, args) => {
  return new Promise((resolve, reject) => {
    const javaprocess = spawn("java", ["-cp", "mysql-connector-j-9.0.0.jar;jdbc/bin", className, ...args]);
    let data1 = "";
    javaprocess.stdout.on('data', (data) => {
      data1 += data.toString();
    })
    javaprocess.on('close', (code) => {
      if (code !== 0) {
        reject(`code rejects with ${code}`)
      }
      else {
        resolve(data1.trim());
      }
    })
  })
}


let c = 0;
router.post('/register', async (req, res) => {
  const username = req.body.username;
  const email = req.body.email;
  const password = req.body.password;
  const formdata = req.body;
  const counts = req.body.img;
  const args1 = [formdata.username];
  const args2 = [formdata.email];
  let args3 = [];
  const args4 = [formdata.name, formdata.username, formdata.email, args3];

  try {
    if (counts === 0) {
      const result1 = await runjava("Auth", args1);
      if ((result1.trim().toLowerCase()) === "username exists") {
        return res.json({ sucess: 'false', message: 'Username exists' });
      }
      return res.json({ sucess: "true", message: 'Username added' });
    }
    if (counts === 1) {
      const result2 = await runjava('email', args2);
      if (result2.trim().toLowerCase() === "email exists") {
        return res.json({ sucess: 'false', message: 'Email exists' });
      }
      return res.json({ sucess: "true", message: 'Email added' });
    }
    if (counts === 2) {
      const salt = await bcrypt.genSalt(10);
      const hashpass = await bcrypt.hash(formdata.password, salt);
      args3 = hashpass;
      return res.json({ sucess: 'true', message: 'Password added' });
    }
    if (counts === 3) {
      const existuser = await User.findOne({ email: email });
      if (!existuser) {
        const newUser = new User({ username, email, password });
        const salt = await bcrypt.genSalt(10);
        const hash = await bcrypt.hash(newUser.password, salt);
        newUser.password = hash;

        await newUser.save();
        console.log("User saved in MongoDB");
      }
      const result3 = await runjava('finalinput', args4);
      console.log(result3);
      return res.redirect("/user/login");
    }

  } catch (error) {
    console.log(error);
    res.status(500).send("Server error");
  }
});

router.post('/forgot', async (req, res) => {
  const email = req.body.forgotusername
  const Password = req.body.Password
  const existemail = await User.findOne({ email: email });
  const existusername = await User.findOne({ username: email });
  if (existemail !== null || existusername !== null) {
    const salt = await bcrypt.genSalt(10);
    const hash = await bcrypt.hash(Password, salt);
    const deleteuser = await User.findOneAndUpdate({ email: email }, { $set: { password: hash } })
    const deleteusername = await User.findOneAndUpdate({ username: email }, { $set: { password: hash } })
  }
  res.redirect('/user/login')
})

router.post('/login', (req, res, next) => {
  passport.authenticate('local', {
    successRedirect: "/dashboard",
    failureRedirect: "/user/login",
  })(req, res, next)
})

router.get('/logout', (req, res) => {
  req.logout(req.user, err => {
    if (err) {
      console.log(err)
    }
  })
  res.redirect('/user/login')
})


module.exports = router;