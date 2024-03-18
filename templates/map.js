// Define the API key
const apiKey = 'AIzaSyAfWvp0dEAr6KzE4QXll0O82fOlfqkWXNk';

// Function to initialize and add the map
function initMap() {
    // The location of Football on Court Africa Durban
    var location = { lat: -29.820594, lng: 31.032515 };

    // The map, centered at Football on Court Africa Durban
    var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: location,
    });

    // The marker, positioned at Football on Court Africa Durban
    var marker = new google.maps.Marker({
        position: location,
        map: map,
    });
}

// Call the initMap function when the window loads
window.onload = function () {
    initMap();
};
