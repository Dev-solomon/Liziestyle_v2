// For categories display

document.addEventListener("DOMContentLoaded", function () {
  const images = [
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1718741635/womendress_z7tivy.png", alt: "women", label: "Women" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1738364305/shoes_smae49.png", alt: "shoes", label: "Shoes" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1738364424/jacket_lnsyvl.png", alt: "men", label: "Men" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1738364655/accessories_qnz1wp.png", alt: "accessories", label: "Accessories" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1718741635/womenbeauty_efrdxz.png", alt: "beauty", label: "Beauty" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1737385456/icons8-household-64_jmypza.png", alt: "household", label: "Household" },
    // Add more images as needed
  ];

  // Select the container element
  const container = document.getElementById("categories");

  // Loop through the array and create HTML elements
  if (container) {
    images.forEach((image) => {
      const imageWrapper = document.createElement("div");
      imageWrapper.className = "category_card";

      const imageContainer = document.createElement("a");
      imageContainer.className = "category_card--image-container";
      // Set the href attribute
      imageContainer.href = "/catalog?product_name=" + image.alt;

      const img = document.createElement("img");
      img.src = image.src;
      img.alt = image.alt;
      img.className = "category_card--img";

      const label = document.createElement("h3");
      label.className = "category_card--label";
      label.textContent = image.label;

      imageContainer.appendChild(img);
      imageWrapper.appendChild(imageContainer);
      imageWrapper.appendChild(label);
      container.appendChild(imageWrapper);
    });
  }



  // for mobile cart show and hide
  const overlay = document.getElementById('overlay');
  const open_cart = document.getElementById('open_cart');
  const open_mobile_cart = document.getElementById('open_mobile_cart');
  const close_cart = document.getElementById('close_cart');
  const cart_box = document.querySelector('#cart_box');

  // Show the cart popup (desktop and mobile)
  const showCart = () => {
    cart_box.style.display = 'block';  // Show the cart box
    overlay.classList.add('active');  // Add overlay
  };

  // Event listeners for opening the cart
  open_cart.addEventListener('click', showCart);
  open_mobile_cart.addEventListener('click', showCart);

  // Close the cart popup
  const closeCart = () => {
    cart_box.style.display = 'none';  // Hide the cart box
    overlay.classList.remove('active');  // Remove overlay
  };

  // Event listener for closing the cart
  close_cart.addEventListener('click', closeCart);

  // Close the cart when clicking outside the cart box
  document.addEventListener('click', (event) => {
    const isClickInsideCart = cart_box.contains(event.target);
    const isClickOnOverlay = overlay === event.target; // Overlay itself
    const isClickOnOpenCart = open_cart.contains(event.target);
    const isClickOnMobileCart = open_mobile_cart.contains(event.target);

    if (!isClickInsideCart && (isClickOnOverlay || !isClickOnOpenCart && !isClickOnMobileCart)) {
      closeCart();
    }
  });

  // Add support for touch events for mobile screens
  document.addEventListener('touchstart', (event) => {
    const isClickInsideCart = cart_box.contains(event.target);
    const isClickOnOverlay = overlay === event.target; // Overlay itself
    const isClickOnOpenCart = open_cart.contains(event.target);
    const isClickOnMobileCart = open_mobile_cart.contains(event.target);

    if (!isClickInsideCart && (isClickOnOverlay || !isClickOnOpenCart && !isClickOnMobileCart)) {
      closeCart();
    }
  });








});






// Get references to the inputs and sliders
const minInput = document.getElementById('minInput');
const maxInput = document.getElementById('maxInput');
const minRange = document.getElementById('minRange');
const maxRange = document.getElementById('maxRange');

// Synchronize slider and input for the minimum price
minRange.addEventListener('input', () => {
  minInput.value = minRange.value;
  if (parseInt(minRange.value) > parseInt(maxRange.value)) {
    maxRange.value = minRange.value;
    maxInput.value = minRange.value;
  }
});

minInput.addEventListener('input', () => {
  const value = parseInt(minInput.value) || 0;
  minRange.value = value;
  if (value > parseInt(maxRange.value)) {
    maxRange.value = value;
    maxInput.value = value;
  }
});

// Synchronize slider and input for the maximum price
maxRange.addEventListener('input', () => {
  maxInput.value = maxRange.value;
  if (parseInt(maxRange.value) < parseInt(minRange.value)) {
    minRange.value = maxRange.value;
    minInput.value = maxRange.value;
  }
});

maxInput.addEventListener('input', () => {
  const value = parseInt(maxInput.value) || 0;
  maxRange.value = value;
  if (value < parseInt(minRange.value)) {
    minRange.value = value;
    minInput.value = value;
  }
});



function updatePageNumber(pageNum) {
  const url = new URL(window.location.href); // Get the current URL
  url.searchParams.set('page_num', pageNum); // Add or update the 'page_num' parameter
  window.location.href = url.toString(); // Redirect to the updated URL
}

function updatePageNumber_nextButton() {
  let pgN = document.getElementById('pgN')
  const url = new URL(window.location.href); // Get the current URL

  // Get the current 'page_num' value from the URL (default to 1 if not present)
  let pageNum = parseInt(url.searchParams.get('page_num')) || 1;

  // Increment the page number by 1
  pageNum += 1;

  // Update the 'page_num' parameter in the URL
  url.searchParams.set('page_num', pageNum);


  // Redirect to the updated URL with the new page number
  window.location.href = url.toString();
}



// for sidebar in mobile menu
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar_menu");
  sidebar.classList.toggle("open");
}

document.getElementById("menu_a").classList.add("active");


function validateEmail() {
  const emailInput = document.getElementById('email');
  const email = emailInput.value;
  const errorMessage = document.getElementById('error-message-email');
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  if (emailRegex.test(email)) {
    errorMessage.textContent = "L'e-mail è valida!";
    errorMessage.style.color = "green";
  } else {
    errorMessage.textContent = "Si prega di inserire un indirizzo email valido.";
    errorMessage.style.color = "red";
    emailInput.value = ""; // Clear the email input field
  }
}

function validatePassword() {
  const passwordInput = document.getElementById('password');
  const password = passwordInput.value;
  const errorMessage = document.getElementById('error-message-pass');
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

  if (passwordRegex.test(password)) {
    errorMessage.textContent = "La password è valida!";
    errorMessage.style.color = "green";
  } else {
    errorMessage.textContent = "La password deve essere lunga almeno 8 caratteri, contenere almeno 1 lettera maiuscola, 1 lettera minuscola, 1 numero e 1 carattere speciale.";
    errorMessage.style.color = "red";
    // passwordInput.value = ""; // Clear the password input field
  }
}


function showPassword() {
  const showpassbtn = document.getElementById('showpassbtn')
  const passwordInput = document.getElementById('password');

  if (passwordInput.type === "password") {
    passwordInput.type = "text"; // Change type to text to show the password
    showpassbtn.innerHTML = "nascondere la password"
  } else {
    passwordInput.type = "password";
    showpassbtn.innerHTML = "mostra la password" // Change type back to password to hide it
  }
}


