$(document).ready(function() {
     function getHashParams() {
		var hashParams = {};
		var e, r = /([^&;=]+)=?([^&;]*)/g,
			q = window.location.hash.substring(1);
		while ( e = r.exec(q)) {
			hashParams[e[1]] = decodeURIComponent(e[2]);
		}
		return hashParams;
	}

	// Extract the token from the URL if you are redirected back to the app
	if (window.location.hash) {
		var params = getHashParams();
		var access_token = params.access_token;
		if (access_token) {
			console.log('Access Token:', access_token);
			// You can now use this access token to make API requests
		}
	}
});

let player;
    
function initializePlayer() {
    
    player = new Spotify.Player({
        name: 'Web Playback SDK Quick Start Player',
        getOAuthToken: cb => cb(access_token),
        volume: 0.5
    });

    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
        // const trackid = this.getAttribute('track_id');
        console.log("Track ID: " + track_id); //get trackid works
        spotifyUri = 'spotify:track:' + track_id;
        console.log("Track Uri: " + spotifyUri);
        playSpotifyTrack(player, spotifyUri, device_id); // Put the TRACKURI here!!!
    });

    player.connect();


    console.log('Spotify Web Playback SDK is ready!');

    $('#startResumeButton').click(function() {
        startResumePlayback(player);
    });
}

window.onload = initializePlayer;

window.onSpotifyWebPlaybackSDKReady = initializePlayer;


function playSpotifyTrack(player, spotifyUri, device_id) {
    player._options.getOAuthToken(access_token => {
        const playOptions = {
            method: 'PUT',
            body: JSON.stringify({ uris: [spotifyUri] }),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            drm: {
                advanced: {
                    'com.widevine.alpha': {
                        'videoRobustness': 'SW_SECURE_CRYPTO',
                        'audioRobustness': 'SW_SECURE_CRYPTO'
                    }
                }
            }
        };
        fetch(`https://api.spotify.com/v1/me/player/play?device_id=${device_id}`, playOptions)
            .then(response => {
                if (response.ok) {
                    console.log("Playback started successfully");
                } else {
                    console.error("Playback failed", response);
                }
            })
            .catch(error => console.error("Error in playback", error));
    });
    player.activateElement();
    player.resume();
}

const playPauseButton = document.getElementById('startResumeButton');

// Function to start/resume playback
function startResumePlayback(player) {
    player.getCurrentState().then(state => {
        if (state && !state.paused) {
            // If playback is not paused, pause it
            player.pause().then(() => {
                console.log('Playback paused');
                playPauseButton.textContent = 'Play';
            }).catch(error => {
                console.error('Error pausing playback:', error);
            });
        } else {
            // If playback is paused, resume it
            player.resume().then(() => {
                console.log('Playback resumed');
                playPauseButton.textContent = 'Pause';
            }).catch(error => {
                console.error('Error resuming playback:', error);
            });
        }
    }).catch(error => {
        console.error('Error getting playback state:', error);
    });
}
