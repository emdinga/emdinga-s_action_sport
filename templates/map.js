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

