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


document.addEventListener('DOMContentLoaded', function () {

    let expand = false;
    
  
  document.querySelector(".Arrow").addEventListener('click' , function(){
  
    expand = !expand;
  
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
  
      document.querySelector(".Arrow").style.transform = expand ? 'rotate(0deg)' : 'rotate(180deg)';
  
    }) 
  
  });
  