window.onSpotifyWebPlaybackSDKReady = () => {
    const token = getAccessToken();
    const player = new Spotify.Player({
        name: 'Your Web Playback SDK Player',
        getOAuthToken: cb => { cb(token); }
    });

    // Add event listeners to the player
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });

    // Connect to the player
    player.connect().then(success => {
        if (success) {
            console.log('The Web Playback SDK successfully connected to Spotify!');
        }
    });
};

// Function to retrieve the access token
async function getAccessToken() {
    const response = await fetch('/get_access_token');
    const data = await response.json();
    console.log('Access token:', data.access_token);
    return data.access_token;
}

// Function to check access token validity
async function checkAccessTokenValidity() {
    const response = await fetch('/check_access_token_validity');
    const data = await response.json();
    console.log('Access token validity:', data.valid);
    return data.valid;
}

// Function to play a track
async function playTrack(trackId, accessToken) {
    try {
        const apiUrl = 'https://api.spotify.com/v1/me/player/play';
        const requestBody = {
            uris: [`spotify:track:${trackId}`]
        };
        response = await fetch(apiUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken
            },
            body: JSON.stringify(requestBody)
        });
        console.log('The repsonse: ', response);

        if (response.ok){
        console.log('Track with ID', trackId, 'is now playing!');}
        else{console.error('Error: ', response.statusText);
        const responsedata = await response.json();
        console.error('More Errors: ', responsedata);

        }
    } catch (error) {
        console.error('Error playing track:', error);
    }
}

// Event listener for play buttons
const playButtons = document.querySelectorAll('.play-button');
playButtons.forEach(button => {
    button.addEventListener('click', async function() { 
        const trackId = this.getAttribute('track_id');
        const accessTokenValid = await checkAccessTokenValidity();
        if (accessTokenValid) {
            const accessToken = await getAccessToken();
            playTrack(trackId, accessToken);
        } else {
            window.location.href = '/homepage';
        }
    });
});
