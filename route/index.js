const express=require('express');
const { ensureAuthentication } = require('../config/off');
const router=express.Router();

router.get('/',(req,res)=>{
    res.render("wel")
})

router.get('/dashboard',ensureAuthentication,(req,res)=>{
    res.render("dashboard",{
       name: req.user.name
    })

})

module.exports=router;