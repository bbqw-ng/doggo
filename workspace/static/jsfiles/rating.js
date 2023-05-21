

function openRate() {
    const menu = document.getElementById('rateMenu');
    menu.style.display = 'block';
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'block';


}

function closeRate() {
    const menu = document.getElementById('rateMenu');
    menu.style.display = 'none';
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'none';
}


const stars = document.querySelectorAll('.star');
let rating = 0;

// Iterate over each star element
stars.forEach((star, index1) => {

    // Add a click event listener to each star
    star.addEventListener('click', () => {
        updateRating(index1 + 1);
        updateGoldStars(index1);
    });

    // Add a mouseover event listener to each star
    star.addEventListener('mouseover', () => {
        highlightStars(index1);
    });

    // Add a mouseout event listener to each star
    star.addEventListener('mouseout', () => {
        removeHighlights();
        updateGoldStars(rating - 1);
    });
});

// Function to update the rating
function updateRating(clickedRating) {
    rating = clickedRating;
    console.log(rating);

    // Create an AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/receive_rating', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response.message); // Display the response message from Flask
        }
    };

    // Send the rating as JSON payload in the request body
    xhr.send(JSON.stringify({ rating: rating }));
}

// Function to highlight stars up to a given index
function highlightStars(index) {
    stars.forEach((star, index2) => {
        if (index2 <= index) {
            star.classList.add('gold');
        }
    });
}

// Function to remove all highlighted stars
function removeHighlights() {
    stars.forEach(star => {
        star.classList.remove('gold');
    });
}

// Function to update gold stars up to a given index
function updateGoldStars(index) {
    stars.forEach((star, index2) => {
        if (index2 <= index) {
            star.classList.add('gold');
        } else {
            star.classList.remove('gold');
        }
    });
}
