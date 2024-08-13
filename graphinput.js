const express=require('express');
const {spawn}=require('child_process')
const app=express();
const port=3000;
app.get('/trial/:num1/:num2/:num3',(req,res)=>{
    let data1='';
    const pyone=spawn('python',['main.py',req.params.num1,req.params.num2,req.params.num3])
    pyone.stdout.on('data',function(data){
        data1+=data.toString();
    })
    pyone.on('close',(code)=>{
        console.log(`child process close all stdio with code ${code}`);
        res.send(data1);
    });
});

app.listen(port,()=>{
    console.log(`app is listening to the ${port} `)
})
