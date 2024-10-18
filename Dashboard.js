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

  const arrowButton = document.querySelector('.Arrow');
  

document.addEventListener("DOMContentLoaded", function () {
  const primarySection = document.querySelector('.primary-section');
  const secondarySection = document.querySelector('.secondary-section');
  const primaryElements = document.querySelector('.primary-elements');
  const secondaryElements = document.querySelector('.secondary-elements');
  
  const servicesDropdown = document.querySelector('.services-dropdown');
  const companyDropdown = document.querySelector('.company-dropdown');
  const servicesLink = document.querySelector('.serv');
  const companyLink = document.querySelector('.comp');

  function showDropdown(dropdown) {
      dropdown.style.display = 'block';
      dropdown.classList.add('show');
      dropdown.classList.remove('hide');
  }

  function hideDropdown(dropdown) {
      dropdown.classList.add('hide');
      dropdown.classList.remove('show');
      
      setTimeout(() => {
          dropdown.style.display = 'none';
      }, 300); 
  }

  primaryElements.style.display = 'block';
  secondaryElements.style.display = 'none';

  primarySection.addEventListener('mouseenter', function() {
      primaryElements.style.display = 'block';  
      secondaryElements.style.display = 'none'; 
  });

  secondarySection.addEventListener('mouseenter', function() {
      secondaryElements.style.display = 'block'; 
      primaryElements.style.display = 'none';    
  });

  servicesDropdown.addEventListener('mouseleave', function() {
      hideDropdown(servicesDropdown);
  });

  servicesLink.addEventListener('mouseenter', function(event) {
      showDropdown(servicesDropdown);
      hideDropdown(companyDropdown);
  });

  companyLink.addEventListener('mouseenter', function(event) {
      showDropdown(companyDropdown);
      hideDropdown(servicesDropdown);
  });

  servicesDropdown.addEventListener('mouseleave', function() {
      hideDropdown(servicesDropdown);
  });

  companyDropdown.addEventListener('mouseleave', function() {
      hideDropdown(companyDropdown);
  });
});
  