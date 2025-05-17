// async function initializePlayer(player) {
//     const token = await getAccessToken();
//     try {
//         await player.connect();
//         console.log('Player initialized successfully');
//     } catch (error) {
//         console.error('Failed to initialize player:', error);
//         throw error;
//     }
// } 

// async function playTrackInBrowser(player, trackUri, metadata) {
//     try {
//         // Delay for 1 second to allow the player to fully initialize
//         await new Promise(resolve => setTimeout(resolve, 1000));

//         // Attempt to initialize the player
//         await initializePlayer(player);

//         // Set the track URI and metadata
//         await player.togglePlay(trackUri, metadata);

//         // Seek to the beginning of the track 
//         await player.seek(0);

//         console.log('Track with URI', trackUri, 'is now playing in the web browser!');
//     } catch (error) {
//         console.error('Error playing track in browser:', error);
//     }
// }

// // Event listener for play buttons
// function addPlayButtonEventListener(player) {
//     const playButtons = document.querySelectorAll('.play-button');
//     playButtons.forEach(button => {
//         button.addEventListener('click', async function() { 
//             const trackId = this.getAttribute('track_id'); // Get the trackId from the button attribute
//             const trackUri = `spotify:track:${trackId}`; // Construct the track URI

//             // Fetch metadata for the track
//             const metadata = await fetchTrackMetadata(trackId);
//             console.log('MetaData: ', metadata)
//             // Check access token validity
//             const accessTokenValid = await checkAccessTokenValidity();
//             if (accessTokenValid) {
//                 // Play the track with metadata
//                 await playTrackInBrowser(player, trackUri, metadata);
//             } else {
//                 window.location.href = '/homepage';
//             }
//         });
//     });
// }

// window.onSpotifyWebPlaybackSDKReady = async () => {
//     const token = await getAccessToken();
//     const player = new Spotify.Player({
//         name: 'Your Web Playback SDK Player',
//         getOAuthToken: cb => { cb(token); }
//     });

//     // Add event listeners to the player
//     player.addListener('initialization_error', ({ message }) => { console.error(message); });
//     player.addListener('authentication_error', ({ message }) => { console.error(message); });
//     player.addListener('account_error', ({ message }) => { console.error(message); });
//     player.addListener('playback_error', ({ message }) => { console.error(message); });

//     // Ready event listener
//     player.addListener('ready', ({ device_id }) => {
//         console.log('The Web Playback SDK successfully connected to Spotify!');
//         addPlayButtonEventListener(player);
//     });

//     // Connect to the player and initialize
//     try {
//         await initializePlayer(player);
//         console.log('Player initialized successfully in try');
//     } catch (error) {
//         console.error('Failed to initialize player:', error);
//         console.log('Player fail to initialized in try');
//     }
// };

// // Function to retrieve the access token
// async function getAccessToken() {
//     const response = await fetch('/get_access_token');
//     const data = await response.json();
//     console.log('Access token:', data.access_token);
//     return data.access_token;
// }

// // Function to check access token validity
// async function checkAccessTokenValidity() {
//     try {
//         const response = await fetch('/check_access_token_validity');
//         const data = await response.json();
//         console.log('Access token validity:', data.valid);
//         return data.valid;
//     } catch (error) {
//         console.error('Error checking access token validity:', error);
//         return false; // Return false if there is an error
//     }
// }

// async function fetchTrackMetadata(trackId) {
//     const accessToken = await getAccessToken();
//     const url = `https://api.spotify.com/v1/tracks/${trackId}`;

//     try {
//         const response = await fetch(url, {
//             headers: {
//                 'Authorization': `Bearer ${accessToken}`
//             }
//         });

//         if (!response.ok) {
//             throw new Error('Failed to fetch track metadata');
//         }

//         const data = await response.json();
//         console.log('Fetched track data:', data);

//         return data;
//     } catch (error) {
//         console.error('Error fetching track metadata:', error);
//         return null; // Return null or handle the error appropriately
//     }
// }








// Function to retrieve the access token
async function getAccessToken() {
    const response = await fetch('/get_access_token');
    const data = await response.json();
    console.log('Access token:', data.access_token);
    return data.access_token;
}

// Define the onSpotifyWebPlaybackSDKReady function
window.onSpotifyWebPlaybackSDKReady = async () => {
    // Initialize the Spotify Web Playback SDK
    const spotifySdk = new Spotify.Player({
        name: 'Web Playback SDK Quick Start Player',
        getOAuthToken: cb => { 
            // Ensure 'token' is defined and contains a valid access token
            const token = getAccessToken();
            cb(token); 
        },
        volume: 1
    });

    // Add event listeners to the player
    spotifySdk.addListener('ready', ({ device_id }) => {
        console.log('The Web Playback SDK is ready to use!');

        // Add event listener to play buttons
        addPlayButtonEventListener();
    });

    spotifySdk.addListener('player_state_changed', state => {
        if (!state) {
        console.log('Player is not playing.');
        return;
        }
        
        // Retrieve current playback state
        const { position, duration, paused, track_window } = state;
        const { current_track } = track_window;
        const { name, uri } = current_track;
        
        console.log('Current Track:', name);
        console.log('Track URI:', uri);
        console.log('Playback Position:', position);
        console.log('Track Duration:', duration);
        console.log('Paused:', paused);
    });

    spotifySdk.addListener('not_ready', ({ device_id }) => {
        console.log('The Web Playback SDK is not ready to use');
    });

    
    // Function to play track in the browser
    async function playTrackInBrowser(trackUri) {
    try {
        // Attempt to initialize the player
        await initializePlayer();

        console.log('track uri before playing: ', trackUri);

        // Add a delay before resuming playback
        setTimeout(async () => {
            try {
                await spotifySdk.resume();
                console.log('Track with URI', trackUri, 'is now playing in the web browser!');
            } catch (error) {
                console.error('Error playing track:', error);
            }
        }, 3000);
    } catch (error) {
        console.error('Error playing track in browser:', error);
    }
    }

    // Function to initialize the player
    async function initializePlayer() {
        try {
            // Connect to the Spotify Web Playback SDK
            await spotifySdk.connect();
            console.log('Player initialized successfully');
        } catch (error) {
            console.error('Failed to initialize player:', error);
            throw error;
        }
    }

    // Event listener for play buttons
    function addPlayButtonEventListener() {
        initializePlayer()
        const playButtons = document.querySelectorAll('.play-button');
        playButtons.forEach(button => {
            button.addEventListener('click', async function() { 
                const trackUri = this.getAttribute('track_id'); // Get the trackId from the button attribute
                console.log("TrackURI Before: " + trackUri);
                // const trackUri = `spotify:track:${trackId}`; // Construct the track URI

                // Check access token validity
                const accessTokenValid = await checkAccessTokenValidity();
                if (accessTokenValid) {
                    // Play the track
                    
                    await playTrackInBrowser(trackUri)
                
                    
                } else {
                    window.location.href = '/homepage';
                }
            });
        });
    }

    // Perform actions when the Spotify Web Playback SDK is ready
    spotifySdk.addListener('initialization_error', ({ message }) => { 
        console.error('Initialization error:', message); 
    });
    spotifySdk.addListener('authentication_error', ({ message }) => { 
        console.error('Authentication error:', message); 
    });
    spotifySdk.addListener('account_error', ({ message }) => { 
        console.error('Account error:', message); 
    });
    spotifySdk.addListener('playback_error', ({ message }) => { 
        console.error('Playback error:', message); 
    });
    

    // Connect to the player and initialize
    try {
        await initializePlayer();
        console.log('Player initialized successfully in try');
    } catch (error) {
        console.error('Failed to initialize player:', error);
        console.log('Player fail to initialized in try');
    }

    
};

// Function to check access token validity
async function checkAccessTokenValidity() {
    try {
        const response = await fetch('/check_access_token_validity');
        const data = await response.json();
        console.log('Access token validity:', data.valid);
        return data.valid;
    } catch (error) {
        console.error('Error checking access token validity:', error);
        return false; // Return false if there is an error
    }
}


// // Function to play a track in the browser
    // async function playTrackInBrowser(trackUri) {
    //     try {
    //         // Attempt to initialize the player
    //         await initializePlayer();
            
    //         console.log('track uri before playing: ', trackUri)
    //         // Play the track directly using spotifySdk.togglePlay()
    //         setTimeout(function() {
    //             // Code to execute after waiting
    //             console.log("Waited for 3000 milliseconds");
    //             spotifySdk.togglePlay(trackUri);
    //         }, 3000);
            

    //         console.log('Track with URI', trackUri, 'is now playing in the web browser!');
    //     } catch (error) {
    //         console.error('Error playing track in browser:', error);
    //     }
    // }

//     async function playTrackWithUri(trackUri) {
//     const accessToken = await getAccessToken();
//     console.log('accessToken in the playTrackWithUri: ', accessToken)
//     try {
//         const response = await fetch('https://api.spotify.com/v1/me/player/play', {
//             method: 'PUT',
//             headers: {
//                 'Authorization': `Bearer ${accessToken}`,
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 uris: [trackUri],
//             }),
//         });

//         if (!response.ok) {
//             throw new Error('Failed to play track');
//         }

//         console.log('Track with URI', trackUri, 'is now playing in the web browser!');
//     } catch (error) {
//         console.error('Error playing track:', error);
//     }
// }
