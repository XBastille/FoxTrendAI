
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

    
  let selectedFrom = null;
  let selectedTo = null;
  let activeInput = null;
  
  const fromBtn = document.getElementById("from-btn");
  const toBtn = document.getElementById("to-btn");
  const calendarContainer = document.querySelector(".calendar-container");
  
  const currentDate = new Date();
  const tomorrow = new Date();
  tomorrow.setDate(currentDate.getDate() + 1);
  
  fromBtn.textContent = `${currentDate.toDateString()}`;
  toBtn.textContent = `${tomorrow.toDateString()}`;
  
  selectedFrom = currentDate;
  selectedTo = tomorrow;
  
  function showCalendar(targetBtn) {
    const btnRect = targetBtn.getBoundingClientRect();
    calendarContainer.style.top = `${btnRect.bottom + window.scrollY}px`;
    calendarContainer.style.left = `${btnRect.left}px`;
    calendarContainer.style.display = "block";
  }
  
  fromBtn.addEventListener("click", function () {
    activeInput = "from";
    showCalendar(fromBtn);
  });
  
  toBtn.addEventListener("click", function () {
    activeInput = "to";
    showCalendar(toBtn);
  });
  
  document.addEventListener("click", function (event) {
    if (!calendarContainer.contains(event.target) && event.target !== fromBtn && event.target !== toBtn) {
      calendarContainer.style.display = "none";
    }
  });
  
  let currentMonth = currentDate.getMonth();
  let currentYear = currentDate.getFullYear();
  const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  
  function updateCalendar() {
    const daysContainer = document.querySelector(".calendar-days");
    daysContainer.innerHTML = ""; 
  
    document.querySelector(".current-month").textContent = `${months[currentMonth]} ${currentYear}`;
    document.querySelector(".year").textContent = currentYear;
  
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
    const numDaysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate(); 
  
    const now = new Date();
  
    for (let i = 0; i < firstDayOfMonth; i++) {
      const emptyDay = document.createElement("span");
      emptyDay.classList.add("calendar-day", "empty-day");
      daysContainer.appendChild(emptyDay);
    }
  
    for (let i = 1; i <= numDaysInMonth; i++) {
      const dayButton = document.createElement("button");
      dayButton.classList.add("calendar-day");
      dayButton.textContent = i;
  
      const thisDate = new Date(currentYear, currentMonth, i);
      if (thisDate > now) {
        dayButton.disabled = true;
        dayButton.style.opacity = 0.5; 
      }
  
      dayButton.addEventListener("click", () => {
        const selectedDate = new Date(currentYear, currentMonth, i).toDateString();
  
        if (activeInput === "from") {
          selectedFrom = new Date(currentYear, currentMonth, i);
          fromBtn.textContent = `${selectedDate}`;
        } else if (activeInput === "to") {
          selectedTo = new Date(currentYear, currentMonth, i);
          toBtn.textContent = `${selectedDate}`;
        }
  
        calendarContainer.style.display = "none"; 
      });
  
      daysContainer.appendChild(dayButton);
    }
  }
  
  document.querySelector(".prev-month").addEventListener("click", () => {
    if (currentMonth === 0) {
      currentMonth = 11;
      currentYear--;
    } else {
      currentMonth--;
    }
    updateCalendar();
  });
  
  document.querySelector(".next-month").addEventListener("click", () => {
    if (currentYear === currentDate.getFullYear() && currentMonth === currentDate.getMonth()) return; 
    if (currentMonth === 11) {
      currentMonth = 0;
      currentYear++;
    } else {
      currentMonth++;
    }
    updateCalendar();
  });
  
  document.querySelector(".prev-year").addEventListener("click", () => {
    currentYear--;
    updateCalendar();
  });
  
  document.querySelector(".next-year").addEventListener("click", () => {
    if (currentYear === currentDate.getFullYear()) return; 
    currentYear++;
    updateCalendar();
  });
  
  updateCalendar();

    
