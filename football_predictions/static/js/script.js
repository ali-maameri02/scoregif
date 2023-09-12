document.addEventListener("DOMContentLoaded", function () {
    const singupForm = document.getElementById('singupForm');
    const loginForm = document.getElementById('loginForm');
    const singupButton = document.getElementById('singupButton');
    const loginButton = document.getElementById('loginButton');
    const btnCloseSingup = document.getElementById('btnCloseSingup');
    const btnCloseLogin = document.getElementById('btnCloseLogin');
    const loginEnter = document.getElementById('loginEnter');
    const singupEnter = document.getElementById('singupEnter');
    const generatMatch = document.getElementById('generatMatch');
    const nextButton = document.getElementById('nextButton');
    const matchTitel = document.getElementById('matchTitel');
    const matchCard = document.getElementById('matchCard');
    const matchesToday = document.getElementById('matchesToday');

    loginEnter.addEventListener('click', function () {
        singupForm.style.display = 'none';
        loginForm.style.display = 'block';
    });

    singupEnter.addEventListener('click', function () {
        loginForm.style.display = 'none';
        singupForm.style.display = 'block';
    });

    singupButton.addEventListener('click', function () {
        singupForm.style.display = 'block';
    });

    loginButton.addEventListener('click', function () {
        loginForm.style.display = 'block';
    });

    btnCloseSingup.addEventListener("click", closeForm);
    btnCloseLogin.addEventListener("click", closeForm);

    function closeForm() {
        loginForm.style.display = 'none';
        singupForm.style.display = 'none';
    }

    const leagueLogos = document.querySelectorAll('.league.btn');

    leagueLogos.forEach(logo => {
        logo.addEventListener('click', () => {
            leagueLogos.forEach(otherLogo => {
                if (otherLogo !== logo) {
                    otherLogo.classList.remove('clicked');
                }
            });
            logo.classList.toggle('clicked');
        });
    });

    const leagues = document.getElementById("leagues");
    const teams = document.getElementById("teams");
    const prevButton = document.getElementById("prevButton");

    function showTeams() {
        leagues.style.opacity = "0";
        leagues.style.transform = "scale(0.95)";
        leagues.style.display = "none"; // Hide leagues
        setTimeout(() => {
            teams.classList.toggle("visible");
        }, 500);
        prevButton.removeAttribute('disabled');
        nextButton.style.display = "none";
        generatMatch.style.display = "block";
        matchTitel.textContent = "Choose the teams";
    }

    function showLeagues() {
        teams.classList.remove("visible");
        leagues.style.opacity = "1";
        leagues.style.transform = "scale(1)";
        leagues.style.display = "flex"; // Display leagues
        prevButton.setAttribute('disabled', 'true');
        nextButton.style.display = "block";
        generatMatch.style.display = "none";
        matchTitel.textContent = "Choose the league";
    }

    // Initially, hide the teams and display leagues
    teams.classList.remove("visible");
    
    // Add an event listener to the "Next" button
    nextButton.addEventListener('click', function () {
        // Check if teams are visible, then show leagues
        if (teams.classList.contains("visible")) {
            showLeagues();
        }
    });

    // Add an event listener to the "Previous" button
    prevButton.addEventListener('click', function () {
        if (teams.classList.contains("visible")) {
            showLeagues(); // Show leagues
        } 
        if(leagues.classList.contains("visible")){
            showTeams();
        }
    });

    // Add an event listener to each team logo
    const teamLogos = document.querySelectorAll('.team.btn');
    let selectedTeams = [];

    teamLogos.forEach(logo => {
        logo.addEventListener('click', () => {
            // Toggle the 'clicked' class on the clicked logo
            logo.classList.toggle('clicked');

            // Add or remove team from selectedTeams array
            if (selectedTeams.includes(logo)) {
                selectedTeams = selectedTeams.filter(team => team !== logo);
            } else {
                if (selectedTeams.length < 2) {
                    selectedTeams.push(logo);
                } else {
                    selectedTeams[0].classList.remove('clicked');
                    selectedTeams.shift();
                    selectedTeams.push(logo);
                }
            }
        });
    });

    generatMatch.addEventListener('click', function () {
        let count = 0;
        teamLogos.forEach(logo => {
            if (logo.classList.contains('clicked')) {
                count++;
            }
        });
        if (count != 2) {
            generatMatch.classList.add('show-after');
        } else {
            generatMatch.classList.remove('show-after');
            matchCard.style.display = 'block';
        }
    });

    nextButton.addEventListener('click', function () {
        let count = 0;
        leagueLogos.forEach(logo => {
            if (logo.classList.contains('clicked')) {
                count++;
            }
        });
        if (count != 1) {
            nextButton.classList.add('show-after');
        } else {
            nextButton.classList.remove('show-after');
            const selectedTournamentId = document.querySelector('.league.btn.clicked').getAttribute('data-league-id');
            fetch(`/get_teams/${selectedTournamentId}/`)  // Make sure the URL matches the URL pattern in Django
                .then(response => response.json())
                .then(data => {
                    // Update the team logos based on the retrieved teams
                    const teamLogos = document.querySelectorAll('.team.btn');
                    teamLogos.forEach(teamLogo => {
                        const teamId = teamLogo.getAttribute('data-team');
                        if (data.teams.some(team => team.id === parseInt(teamId))) {
                            teamLogo.style.display = 'block';
                
                        } else {
                            teamLogo.style.display = 'none';
                        }
                    });
                    showTeams(); 
                     // Call showTeams after updating team logos
                });
        }
    });

  

    matchesToday.querySelectorAll('.match-today').forEach(match => {
        match.addEventListener('click', function () {
            matchCard.style.display = 'block';
        });
    });
});
