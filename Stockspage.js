document.querySelector(".Arrow").addEventListener('click' , function(){
    document.querySelectorAll(".Icon-items").forEach(function(item){
          const iconName = item.querySelector('.icon-name');
          const nameText = item.getAttribute('data-name');

          if(iconName.style.display === "none" || iconName.style.display === ' ') {
            iconName.textContent = nameText;
            iconName.style.display = 'inline-block';
          }else{
            iconName.style.display = 'none';
          }
             
          
    })

  }) 

document.querySelector(".Arrow2").addEventListener('click' , function(){
   const ARROW = document.querySelector('.Arrow');
   const iconName = item.querySelector('.icon-name');
   const nameText = item.getAttribute('data-name');

   ARROW.style.display = "none";

})  
  
  document.querySelector(".sum").addEventListener('click' , function(){
    const SUMMARY = document.querySelector('.sum');
    const CHART = document.querySelector('.cha');
    const HISTO = document.querySelector('.histo');
    const STAT = document.querySelector('.stat');
    const PRO = document.querySelector('.pro');
    SUMMARY.style.backgroundColor= " rgb(96, 0, 147)";
    HISTO.style.backgroundColor = "black";
    PRO.style.backgroundColor = "black";
    CHART.style.backgroundColor = "black";
    SUMMARY.border = "10px solid rgb(96, 0, 147)";
    
})

  document.querySelector(".cha").addEventListener('click' , function(){
    const SUMMARY = document.querySelector('.sum');
    const CHART = document.querySelector('.cha');
    const HISTO = document.querySelector('.histo');
    const STAT = document.querySelector('.stat');
    const PRO = document.querySelector('.pro');
    SUMMARY.style.backgroundColor= "black";
    HISTO.style.backgroundColor = "black";
    STAT.style.backgroundColor = "black";
    PRO.style.backgroundColor = "black";
    CHART.style.backgroundColor = "rgb(96, 0, 147)";
})

document.querySelector(".histo").addEventListener('click' , function(){
  const SUMMARY = document.querySelector('.sum');
  const CHART = document.querySelector('.cha');
  const HISTO = document.querySelector('.histo');
  const STAT = document.querySelector('.stat');
  const PRO = document.querySelector('.pro');
  SUMMARY.style.backgroundColor= "black";
  HISTO.style.backgroundColor = "rgb(96, 0, 147)";
  STAT.style.backgroundColor = "black";
  PRO.style.backgroundColor = "black";
  CHART.style.backgroundColor = "black";
})

document.querySelector(".stat").addEventListener('click' , function(){
  const SUMMARY = document.querySelector('.sum');
  const CHART = document.querySelector('.cha');
  const HISTO = document.querySelector('.histo');
  const STAT = document.querySelector('.stat');
  const PRO = document.querySelector('.pro');
  SUMMARY.style.backgroundColor= "black";
  HISTO.style.backgroundColor = "black";
  STAT.style.backgroundColor = "rgb(96, 0, 147)";
  PRO.style.backgroundColor = "black";
  CHART.style.backgroundColor = "black";
})

document.querySelector(".pro").addEventListener('click' , function(){
  const SUMMARY = document.querySelector('.sum');
  const CHART = document.querySelector('.cha');
  const HISTO = document.querySelector('.histo');
  const STAT = document.querySelector('.stat');
  const PRO = document.querySelector('.pro');
  SUMMARY.style.backgroundColor= "black";
  HISTO.style.backgroundColor = "black";
  STAT.style.backgroundColor = "black";
  PRO.style.backgroundColor = "rgb(96, 0, 147)";
  CHART.style.backgroundColor = "black";
})

function changeReadMore(){
  const morecontent = document.querySelector('.More-content');
  const showMoreBtn = document.querySelector('.show-more-btn');

  if(morecontent.style.display === "none" || morecontent.style.display === " "){
    morecontent.style.display = "block";
    showMoreBtn.textContent = "Show Less";
  }else{
    morecontent.style.display = 'none';
    showMoreBtn.textContent = 'Show More';
  }
}

   /* const iconMenu = document.querySelector('.Icons');
    
    // Toggle the expand class to push the right border and show names
    if (iconMenu.classList.contains('expand')) {
        iconMenu.classList.remove('expand');
    } else {
        iconMenu.classList.add('expand');
    }
    */

    let currentSlide = 0;
    const slideWidth = 210; 
    const visibleSlides = 5;
    const totalSlides = document.querySelectorAll('.company-box').length;
    const slider = document.getElementById('slider');

    function slide(direction) {
        currentSlide += direction;
        const maxSlide = totalSlides - visibleSlides;

        if (currentSlide < 0) {
            currentSlide = 0; 
        }
        if (currentSlide > maxSlide) {
            currentSlide = maxSlide; 
        }
        slider.style.transform = `translateX(${-currentSlide * slideWidth}px)`;
    }
