const express=require('express');
const { spawn }=require('child_process');
const app=express();
const port=3000;

app.get('/trial/:numCompanies/:tickers/:startDate/:endDate', (req, res) => {
    let data1='';
    const tickers=req.params.tickers.split(','); 
    const args=[req.params.numCompanies, ...tickers, req.params.startDate, req.params.endDate];
    const pyone=spawn('python', ['trial.py', ...args]);
    pyone.stdout.on('data', function (data) {
        data1+=data.toString();
    });
    pyone.on('close', (code)=>{
        console.log(`child process close all stdio with code ${code}`);
        res.send(data1);
    });
});
app.listen(port, ()=>{
    console.log(`app is listening to the ${port}`);
});
