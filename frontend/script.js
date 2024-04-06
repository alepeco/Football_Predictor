// script.js
function makePrediction() {
    const teamLogos = {
        "Athletic Club": "logos/AthleticClub.png",
        "Almería": "logos/Almeria.png",
        "Alavés": "logos/Alaves.png",
        "Atlético Madrid": "logos/AtleticoMadrid.png",
        "Barcelona": "logos/Barcelona.png",
        "Betis": "logos/Betis.png",
        "Cádiz": "logos/Cadiz.png",
        "Celta Vigo": "logos/CeltaVigo.png",
        "Getafe": "logos/Getafe.png",
        "Girona": "logos/Girona.png",
        "Granada": "logos/Granada.png",
        "Las Palmas": "logos/LasPalmas.png",
        "Mallorca": "logos/Mallorca.png",
        "Osasuna": "logos/Osasuna.png",
        "Rayo Vallecano": "logos/RayoVallecano.png",
        "Real Madrid": "logos/RealMadrid.png",
        "Real Sociedad": "logos/RealSociedad.png",
        "Sevilla": "logos/Sevilla.png",
        "Valencia": "logos/Valencia.png",
        "Villareal": "logos/Villarreal.png"
    };
    document.getElementById('loadingIcon').style.display = 'block';
    document.getElementById('predictionResult').innerHTML = '';
    const teamAName = document.getElementById('team_a_name').value;
    const teamBName = document.getElementById('team_b_name').value;
    const teamALogo = document.getElementById('teamALogo');
    const teamBLogo = document.getElementById('teamBLogo');
    teamALogo.style.display = 'none';
    teamBLogo.style.display = 'none';
    var venue = document.getElementById('venue').value;

    var data = {
        team_a_name: teamAName,
        team_b_name: teamBName,
        venue: venue
    };

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
    
        if (teamALogo && teamBLogo) {
            teamALogo.src = teamLogos[teamAName];
            teamBLogo.src = teamLogos[teamBName];
    
            teamALogo.style.display = 'inline';
            teamBLogo.style.display = 'inline';
        } else {
            console.error('Logo elements not found');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('loadingIcon').style.display = 'none';
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const teamASelect = document.getElementById('team_a_name');
    const teamBSelect = document.getElementById('team_b_name');
    const teamALogo = document.getElementById('teamALogo');
    const teamBLogo = document.getElementById('teamBLogo');
    
    if (!teamALogo || !teamBLogo) {
        console.error('Logo elements not found. Ensure they are defined in the HTML.');
        return;
    }
    
    function updateTeamOptions(selectElementToChange, excludeTeamValue, currentSelection) {
        const teams = [
            "Barcelona", "Rayo Vallecano", "Mallorca", "Getafe",
            "Sevilla", "Cádiz", "Real Madrid", "Atlético Madrid",
            "Real Sociedad", "Girona", "Athletic Club", "Betis",
            "Valencia", "Villareal", "Las Palmas", "Osasuna",
            "Alavés", "Celta Vigo", "Granada", "Almería"
        ];

        teams.sort();

        const shouldRetainSelection = currentSelection && currentSelection !== excludeTeamValue;
        
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

    updateTeamOptions(teamASelect, teamBSelect.value, teamASelect.value);
    updateTeamOptions(teamBSelect, teamASelect.value, teamBSelect.value);
});
