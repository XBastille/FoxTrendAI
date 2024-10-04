document.querySelector(".StockButton").addEventListener("click" , function(){
    const StockContent = document.getElementById("StockContent");
    const LoanContent = document.getElementById("LoanContent");
    const StockButton = document.querySelector(".StockButton");
    const loanButton = document.querySelector(".loanButton");
    const HouseButton = document.querySelector(".HouseButton");
    const carButton = document.querySelector(".carButton");


    LoanContent.style.display = "none";
    LoanContent.style.opacity = 0;
    LoanContent.style.animation = "none";
    loanButton.style = "none";


    CarContent.style.display = "none";
    CarContent.style.opacity = 0;
    carButton.style = "none";

    HouseContent.style.display = "none";
    HouseContent.style.opacity = 0;
    HouseButton.style = "none";

    let styles = `
      border-bottom-width: 10px;
      border-bottom-color: #AA336A;
      border-bottom-width:medium; `

    StockContent.style.display = "block";
    StockContent.style.opacity = 1;
    StockContent.style.animation ="SlideFromRight 1s ease forwards" ;
    StockButton.style = styles; 
    StockButton.style.color = "white";

 });

document.querySelector(".loanButton").addEventListener("click" , function(){
   /* const LoanContent = document.getElementById("LoanContent");
    const StockContent = document.getElementById("StockContent");*/
   const StockButton = document.querySelector(".StockButton");
    const loanButton = document.querySelector(".loanButton");
    const carButton = document.querySelector(".carButton");
    const HouseButton = document.querySelector(".HouseButton");

    StockContent.style.display = "none";
    StockContent.style.opacity = 0;
    StockButton.style = "none";
    StockButton.style.borderBottom = "none";
   /* StockContent.style.animation ="none";
    StockContent.style.animation = "SlideFromLeft 1s  forwards";*/
    
    
    LoanContent.style.display = "block";
    LoanContent.style.animation = "SlideFromRight 1s  forwards";
    LoanContent.style.opacity = 1; 
   
    CarContent.style.display = "none";
    CarContent.style.opacity = 0;
    carButton.style = "none";

    HouseContent.style.display = "none";
    HouseContent.style.opacity = 0;
    HouseButton.style = "none";



    let styles = `
      border-bottom-width: 10px;
      border-bottom-color: #AA336A;
      border-bottom-width:medium; 
      color:white;`

    loanButton.style = styles;
    
    StockButton.style.borderBottom = "none";


}); 

document.querySelector(".carButton").addEventListener("click" , function(){
    const StockContent = document.getElementById("StockContent");
    const LoanContent = document.getElementById("LoanContent");
    const CarContent = document.getElementById("CarContent");
    const StockButton = document.querySelector(".StockButton");
    const loanButton = document.querySelector(".loanButton");
    const carButton = document.querySelector(".carButton");
    const HouseButton = document.querySelector(".HouseButton");


    
    StockContent.style.display = "none";
    StockContent.style.opacity = 0;
    StockContent.style.animation = "none;"
    StockButton.style = "none";
    StockButton.style.borderBottom = "none";
    
    LoanContent.style.display = "none";
   LoanContent.style.opacity = 0;
    LoanContent.style.animation = "none";
    loanButton.style = "none";

    HouseContent.style.display = "none";
    HouseContent.style.opacity = 0;
    HouseContent.style.animation = "none";
    HouseButton.style = "none";


    CarContent.style.display = "block"
    CarContent.style.animation = "SlideFromRight 1s ease forwards";
    CarContent.style.opacity = 1;
    carButton.style.color = "white";


    let styles = `
    border-bottom-width: 10px;
    border-bottom-color:  #AA336A;
    border-bottom-width:medium;
    color:white; `

    carButton.style = styles;
 


}); 

document.querySelector(".HouseButton").addEventListener("click" , function(){
    const StockContent = document.getElementById("StockContent");
    const LoanContent = document.getElementById("LoanContent");
    const CarContent = document.getElementById("CarContent");
    const HouseContent = document.getElementById("HouseContent")
    const StockButton = document.querySelector(".StockButton");
    const loanButton = document.querySelector(".loanButton");
    const carButton = document.querySelector(".carButton");
    const HouseButton = document.querySelector(".HouseButton");
    
    StockContent.style.display = "none";
    StockContent.style.opacity = 0;
    StockContent.style.animation = "none";
    StockButton.style = "none";
    StockButton.style.borderBottom = "none";
    
    LoanContent.style.display = "none";
    LoanContent.style.opacity = 0;
    LoanContent.style.animation = "none";
    loanButton.style = "none";

    CarContent.style.display = "none";
    CarContent.style.opacity = 0;
    CarContent.style.animation = "none";
    carButton.style = "none";

    HouseContent.style.display = "block";
    HouseContent.style.opacity = 1;
    HouseContent.style.animation = "SlideFromRight 1s ease forwards";
    HouseButton.style.color = "white";


    let styles = `
    border-bottom-width: 10px;
    border-bottom-color:  #AA336A;
    border-bottom-width:medium;
    color:white; `

    HouseButton.style = styles;


});



document.addEventListener('DOMContentLoaded', function() {
    const quote1 = document.querySelector('.quote1');
 
    const observer2 = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0 });

    observer2.observe(quote1);

}); 

document.addEventListener('scroll' , function(){
    const text = document.querySelector('.quote-text');
    const textposi = text.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if(textposi < windowHeight && !text.classList.add('visible')){
        text.classList.add('visible');
    }
})

document.querySelector('.footer-button').addEventListener("click" , function(event) {

    document.querySelector('.footer-button').style.border = "4px solid white";
    event.stopPropagation();

});


document.addEventListener("scroll", function() {
    const video=document.getElementById("background-video");
    const servicesSection=document.querySelector(".industries").offsetTop;
    const scrollPosition=window.scrollY;
    const windowHeight=window.innerHeight;
    const initialBrightness=0.4;  
    let darkenFactor=Math.min(scrollPosition / servicesSection, 1);
    video.style.filter=`brightness(${initialBrightness - darkenFactor*initialBrightness})`; 
    if (scrollPosition>=servicesSection - windowHeight) {
        let fadeOutFactor=Math.min((scrollPosition - (servicesSection - windowHeight))/windowHeight, 1);
        video.style.opacity=`${1-fadeOutFactor}`; 
    } else {
        video.style.opacity="1"; 
    }
});

document.addEventListener('click' , function(){

    document.querySelector('.footer-button').style.border = "none";

})

document.addEventListener('scroll' , function(){
    const btn = document.querySelector('.footer-button');
    const btnposi =  btn.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if(btnposi < windowHeight && !btn.classList.contains('show')){
             btn.classList.add('show');
    }

});

document.addEventListener('scroll' , function(){
    const block = document.querySelectorAll('.footer-block');
    
    const windowHeight = window.innerHeight;

    block.forEach(function(block){

    const blockposi = block.getBoundingClientRect().top;

    if(blockposi < windowHeight && !block.classList.contains('face')){
        block.classList.add('face');
    }

   });
    
});