const express=require('express');
const app=express();
const port=3000;


app.set('view engine', 'hbs');

app.use(express.urlencoded({ extended: false }))

app.use(express.static('public'))

app.use("/",require("./route/graph"))

app.listen(port, ()=>{
    console.log(`app is listening to the ${port}`);
});
