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

    
    window.onSpotifyWebPlaybackSDKReady = () => {
        $('#playerbutton').click(function() {


        const player = new Spotify.Player({
            name: 'Web Playback SDK Quick Start Player',
            getOAuthToken: cb => cb(access_token),
            volume: 0.5
        });

        player.addListener('ready', ({ device_id }) => {
            console.log('Ready with Device ID', device_id);
            playSpotifyTrack(player, 'spotify:track:0K6yUnIKNsFtfIpTgGtcHm?si=8f0a2526f14a4db4', device_id); // Put the TRACKURI here!!!
        });

        player.connect();
        });
    }
});

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











