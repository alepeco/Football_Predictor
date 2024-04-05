// script.js
function makePrediction() {
    document.getElementById('loadingIcon').style.display = 'block';
    document.getElementById('predictionResult').innerHTML = '';
    var teamAName = document.getElementById('team_a_name').value;
    var teamBName = document.getElementById('team_b_name').value;
    var venue = document.getElementById('venue').value;

    // Create the request body
    var data = {
        team_a_name: teamAName,
        team_b_name: teamBName,
        venue: venue
    };

    // Make an AJAX request to the Flask backend
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingIcon').style.display = 'none';
        console.log('Success:', data);
        document.getElementById('predictionResult').innerHTML = `Prediction: ${data.confidence}, ${data.outcome}`;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('loadingIcon').style.display = 'none';
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const teamASelect = document.getElementById('team_a_name');
    const teamBSelect = document.getElementById('team_b_name');
    
    function updateTeamOptions(selectElementToChange, excludeTeamValue, currentSelection) {
        const teams = [
            "Barcelona", "Rayo Vallecano", "Mallorca", "Getafe",
            "Sevilla", "Cádiz", "Real Madrid", "Atlético Madrid",
            "Real Sociedad", "Girona", "Athletic Club", "Betis",
            "Valencia", "Villareal", "Las Palmas", "Osasuna",
            "Alavés", "Celta Vigo", "Granada", "Almería"
        ];

        // Sort teams alphabetically
        teams.sort();

        // Save the current selection if not excluded
        const shouldRetainSelection = currentSelection && currentSelection !== excludeTeamValue;
        
        // Clear current options and repopulate
        selectElementToChange.innerHTML = '';
        teams.forEach(team => {
            if (team !== excludeTeamValue) {
                const option = document.createElement("option");
                option.value = team;
                option.text = team;
                if (shouldRetainSelection && team === currentSelection) {
                    option.selected = true;
                }
                selectElementToChange.add(option);
            }
        });
    }
    
    teamASelect.addEventListener('change', function() {
        updateTeamOptions(teamBSelect, this.value, teamBSelect.value);
    });

    teamBSelect.addEventListener('change', function() {
        updateTeamOptions(teamASelect, this.value, teamASelect.value);
    });

    // Initial population
    updateTeamOptions(teamASelect, teamBSelect.value, teamASelect.value);
    updateTeamOptions(teamBSelect, teamASelect.value, teamBSelect.value);
});
