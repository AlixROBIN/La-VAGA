document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("menu-toggle").addEventListener("click", function() {
        var menu = document.getElementById("departement-menu");
        if (menu.style.display === "none" || menu.style.display === "") {
            menu.style.display = "block";
        } else {
            menu.style.display = "none";
        }
    });

    document.getElementById("select-all").addEventListener("click", function() {
        var checkboxes = document.querySelectorAll('#departement-menu input[type="checkbox"]');
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = true;
        });
    });

    document.getElementById("deselect-all").addEventListener("click", function() {
        var checkboxes = document.querySelectorAll('#departement-menu input[type="checkbox"]');
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = false;
        });
    });
});

function toggleRegion(regionId) {
    var elements = document.getElementsByClassName(regionId);
    for (var i = 0; i < elements.length; i++) {
        elements[i].classList.toggle("hidden");
    }
}

function toggleDepartment(departmentId) {
    var elements = document.getElementsByClassName(departmentId);
    for (var i = 0; i < elements.length; i++) {
        elements[i].classList.toggle("hidden");
    }
}

function showMarker(lat, lon, content) {
    var popup = L.popup()
        .setLatLng([lat, lon])
        .setContent(content)
        .openOn(map);
}
