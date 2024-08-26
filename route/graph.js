
const express=require('express');
const router = express.Router();
const { spawn }=require('child_process');



router.get("/",(req,res)=>{
    res.render("template")
})
 


router.post('/trials', (req, res) => {
    let data1='';
    
    const numCompanies=req.body.numCompanies;
    const startDate=req.body.startDate;
    const endDate=req.body.endDate;
    const tickers=req.body.tickers.split(','); 
    const args=[numCompanies, ...tickers, startDate, endDate];

    console.log("Arguments :"+args)

    const pyone=spawn('python', ['./main.py', ...args]);
    pyone.stdout.on('data', function (data) {
        data1+=data.toString();
    });

    pyone.on('close', (code)=>{
        console.log(`child process close all stdio with code ${code}`);
        res.send(data1);
    });
});


module.exports=router;
