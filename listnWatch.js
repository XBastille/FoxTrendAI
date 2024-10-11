document.querySelector('.filter-icon').addEventListener('click', function() {
    const filterBox = document.getElementById('filterBox');
    filterBox.style.display = filterBox.style.display === 'none' ? 'block' : 'none';
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    const filterIcon = document.querySelector('.filter-icon');
    const filterBox = document.getElementById('filterBox');
    const minPriceInput = document.getElementById('minPrice');
    const maxPriceInput = document.getElementById('maxPrice');
    const priceRangeSpan = document.getElementById('priceRange');
    const clearFiltersBtn = document.getElementById('clearFilters');
    const percentageChangeSelect = document.getElementById('percentageChange');
    const sortBySelect = document.getElementById('sortBy');
    const quickFilterButtons = document.querySelectorAll('.quick-filter');
    const customMinInput = document.getElementById('customMin');
    const customMaxInput = document.getElementById('customMax');
    const applyFiltersBtn = document.getElementById('applyFilters');
  
    filterIcon.addEventListener('click', function() {
        filterBox.classList.toggle('show');
        filterBox.classList.toggle('hide');
    });
  
    function updatePriceRange() {
        priceRangeSpan.textContent = `$${minPriceInput.value} - $${maxPriceInput.value}`;
    }
  
    function validatePriceRange() {
      if (parseInt(minPriceInput.value) > parseInt(maxPriceInput.value)) {
          maxPriceInput.value = minPriceInput.value;
      }
      updatePriceRange();
    }
  
    function validateCustomRange() {
      let min = parseFloat(customMinInput.value);
      let max = parseFloat(customMaxInput.value);
      
      min = Math.max(-100, Math.min(100, min));
      max = Math.max(-100, Math.min(100, max));
      
      if (min > max) {
          max = min;
      } else if (max < min) {
          min = max;
      }
      
      customMinInput.value = min;
      customMaxInput.value = max;
    }
  
    minPriceInput.addEventListener('input', validatePriceRange);
    maxPriceInput.addEventListener('input', validatePriceRange);
    customMinInput.addEventListener('input', validateCustomRange);
    customMaxInput.addEventListener('input', validateCustomRange);
  
    quickFilterButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('selected');
        });
    });
  
    clearFiltersBtn.addEventListener('click', function() {
        minPriceInput.value = 0;
        maxPriceInput.value = 1000;
        updatePriceRange();
        percentageChangeSelect.value = '';
        sortBySelect.value = 'priceAsc';
        customMinInput.value = '';
        customMaxInput.value = '';
        quickFilterButtons.forEach(button => button.classList.remove('selected'));
    });
  
    updatePriceRange();
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    const avatarEdit = document.querySelector('.avatar-edit');
    const avatarPopup = document.querySelector('.avatar-popup');
  
    avatarEdit.addEventListener('click', function() {
      console.log('Avatar edit clicked');
      if (avatarPopup) {
        avatarPopup.classList.toggle('show');
        if (avatarPopup.classList.contains('show')) {
          avatarPopup.style.display = 'flex';
          setTimeout(() => avatarPopup.style.opacity = '1', 10); 
          console.log('Avatar popup displayed');
        } else {
          avatarPopup.style.opacity = '0';
          setTimeout(() => avatarPopup.style.display = 'none', 500); 
          console.log('Avatar popup hidden');
        }
      } else {
        console.log('Avatar popup not found');
      }
    });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
      const avatarOptions = document.querySelectorAll('.avatar-option');
      const selectButton = document.querySelector('.select-button');
      const profileAvatar = document.querySelector('.avatar');
      const avatarPopup = document.querySelector('.avatar-popup');
  
      const initialSelectedAvatar = document.querySelector('.avatar-option.selected');
      if (initialSelectedAvatar) {
          profileAvatar.src = initialSelectedAvatar.src;
      }
  
      avatarOptions.forEach(option => {
          option.addEventListener('click', function() {
              avatarOptions.forEach(opt => opt.classList.remove('selected'));
              this.classList.add('selected');
          });
      });
  
      avatarOptions.forEach(option => {
          option.addEventListener('click', function() {
              avatarOptions.forEach(opt => opt.classList.remove('selected'));
              this.classList.add('selected');
          });
      });
  
      selectButton.addEventListener('click', function() {
          const selectedAvatar = document.querySelector('.avatar-option.selected');
          if (selectedAvatar) {
              profileAvatar.src = selectedAvatar.src;
              avatarPopup.style.display = 'none';
          }
      });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    const accountItems = document.querySelectorAll('.account-item');
  
    accountItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('connected');
            const status = this.querySelector('.connection-status');
            if (this.classList.contains('connected')) {
                status.textContent = 'Connected';
            } else {
                status.textContent = 'Not Connected';
            }
        });
    });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
      const connectButtons = document.querySelectorAll('.connect-button');
  
      connectButtons.forEach(button => {
          button.addEventListener('click', function() {
              if (this.classList.contains('loading')) return;
  
              this.classList.add('loading');
              this.textContent = '';
  
              setTimeout(() => {
                  this.classList.remove('loading');
                  if (this.classList.contains('connected')) {
                      this.classList.remove('connected');
                      this.textContent = 'Connect';
                  } else {
                      this.classList.add('connected');
                      this.textContent = 'Connected';
                  }
              }, 2000);
          });
      });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.querySelector('.edit-button');
    const profileFields = document.querySelectorAll('.profile-field');
    const avatarUsername = document.querySelector('.profile-header h1'); 
    const confirmPasswordField = document.querySelector('.confirm-password'); 
  
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
  
    function clearError(field) {
        const errorMessage = field.querySelector('.error-message');
        if (errorMessage) errorMessage.remove();
        field.querySelectorAll('input').forEach(input => input.classList.remove('error'));
    }
  
    editButton.addEventListener('click', function() {
        if (this.textContent.trim() === 'Edit Info') {
            profileFields.forEach(field => {
                const span = field.querySelector('span');
                const input = field.querySelector('input');
                if (span && input) {
                    span.style.display = 'none'; 
                    input.style.display = 'inline-block'; 
                }
            });
  
            confirmPasswordField.style.display = 'flex'; 
            this.textContent = 'Save Info'; 
        } else {
            let isValid = true;
            let updatedUsername = '';
  
            profileFields.forEach(field => {
                clearError(field); 
                const span = field.querySelector('span');
                const input = field.querySelector('input');
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.style.color = 'red';
                errorMessage.style.fontSize = '12px';
  
                if (input) {
                    if (input.value.trim() === '') {
                        isValid = false;
                        input.classList.add('error');
                        errorMessage.textContent = 'This field cannot be empty';
                        field.appendChild(errorMessage);
                    } else if (input.type === 'email' && !validateEmail(input.value)) {
                        isValid = false;
                        input.classList.add('error');
                        errorMessage.textContent = 'Please enter a valid email address';
                        field.appendChild(errorMessage);
                    } else if (span) {
                        span.textContent = input.type === 'password' ? '••••••••' : input.value; 
                        if (input.type === 'text' && field.querySelector('label').textContent === 'Username:') {
                            updatedUsername = input.value;
                        }
                    }
                }
            });
            const passwordField = document.querySelector('.profile-field input[type="password"]');
            const confirmPasswordInput = document.querySelector('.confirm-password input');
            if (passwordField.value !== confirmPasswordInput.value) {
                isValid = false;
                confirmPasswordInput.classList.add('error');
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.textContent = 'Passwords do not match';
                errorMessage.style.color = 'red';
                confirmPasswordInput.parentElement.appendChild(errorMessage);
            }
            if (isValid) {
                profileFields.forEach(field => {
                    const span = field.querySelector('span');
                    const input = field.querySelector('input');
                    if (span && input) {
                        input.style.display = 'none'; 
                        span.style.display = 'inline-block'; 
                    }
                });
  
                if (updatedUsername) {
                    avatarUsername.textContent = updatedUsername;
                }
  
                confirmPasswordField.style.display = 'none'; 
  
                this.textContent = 'Edit Info'; 
            }
        }
    });
  
    profileFields.forEach(field => {
        const inputs = field.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => clearError(field));
        });
    });
  });
  
  
  const arrowButton = document.querySelector('.Arrow');
  const iconsList = document.querySelector('.icons');
  
  arrowButton.addEventListener('click', () => {
      iconsList.classList.toggle('open');
      iconsList.classList.toggle('closed');
  });
  
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
  
  document.addEventListener('DOMContentLoaded', function () {
  
    const dateRangeButtons = document.querySelectorAll('.date-range-button');
    const showFullGraphBtn = document.getElementById('show-full-graph');
  
    dateRangeButtons.forEach(button => {
      button.addEventListener('click', () => {
        dateRangeButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
      });
    });
  
    showFullGraphBtn.addEventListener('click', () => {
    });
  
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
  
    
  
  
  
      