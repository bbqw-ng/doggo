const stars = document.querySelectorAll('.star');
let rating = 0;

// Iterate over each star element
stars.forEach((star, index1) => {

    // Add a click event listener to each star
    star.addEventListener('click', () => {

        // Iterate over each star again to determine the rating and apply color
        stars.forEach((star, index2) => {

            // Add 'gold' class to stars up to and including the clicked star index,
            // and remove 'gold' class from stars after the clicked star index
            index1 >= index2 ? star.classList.add('gold') : star.classList.remove('gold');

            // Calculate the rating based on the clicked star index
            rating = index1 + 1;
            console.log(rating);

        });
    });
});