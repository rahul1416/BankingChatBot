let mediaRecorder;
let socket;
let stopwatchInterval;
let remainingTime = 9;
// let totalAccuracy = 0;
// let totalLatency = 0;
// let transcriptCount = 0;

const startStopwatch = () => {
    countdownInterval = setInterval(() => {
        remainingTime -= 1;
        if (remainingTime >= 0) {
            updateStopwatch();
        } else {
            closeConnection();
        }
    }, 1000);
};

const updateStopwatch = () => {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    document.querySelector('#stopwatch').textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
};

const stopStopwatch = () => {
    clearInterval(countdownInterval);
};

const resetStopwatch = () => {
    remainingTime = 9;
    updateStopwatch();
};


const askpermission = () => {
    console.log("Yeah we started");

    // Close the existing WebSocket connection if it exists
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
    }

    // Stop the existing MediaRecorder if it exists
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }

    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        if (!MediaRecorder.isTypeSupported('audio/webm'))
            return alert('Browser not supported')

        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm',
        });

        socket = new WebSocket(`ws://${window.location.host}/listen`);

        socket.onopen = () => {
            document.querySelector('#status').textContent = 'Connected';
            startStopwatch();

            mediaRecorder.addEventListener('dataavailable', async (event) => {
                if (event.data.size > 0 && socket.readyState === WebSocket.OPEN) {
                    socket.send(event.data);
                }
            });

            mediaRecorder.start(250);

            setTimeout(() => {
                closeConnection();
            }, 9000);  // 90 seconds
        };

        socket.onmessage = (message) => {
            const received = JSON.parse(message.data);
            if (received) {
                console.log("This is what we recieved",received)
                // const accuracy = received['accuracy'];
                // const latency = received['latency'];

                // document.querySelector('#transcript').value += ' ' + received['transcript'];
                // document.querySelector('#accuracy').textContent = accuracy.toFixed(2);
                // document.querySelector('#latency').textContent = latency.toFixed(2);

                // // Calculate and update average accuracy and latency
                // totalAccuracy += accuracy;
                // totalLatency += latency;
                // transcriptCount++;

                // const averageAccuracy = (totalAccuracy / transcriptCount).toFixed(2);
                // const averageLatency = (totalLatency / transcriptCount).toFixed(2);

                // document.querySelector('#averageAccuracy').textContent = averageAccuracy;
                // document.querySelector('#averageLatency').textContent = averageLatency;
            }
        };

        socket.onclose = () => {
            console.log({ event: 'onclose' });
            stopStopwatch();
        };

        socket.onerror = (error) => {
            console.log({ event: 'onerror', error });
        };
    });
};

const clearTranscript = () => {
    console.log("clearTranscript")
    // document.querySelector('#transcript').value = '';
    // document.querySelector('#accuracy').textContent = '0';
    // document.querySelector('#latency').textContent = '0';
};

const closeConnection = () => {
    // Close the existing WebSocket connection if it exists
    try {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
    } catch {
        console.log("group_discard_Error");
    }
    // Stop the existing MediaRecorder if it exists
    try {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
    } catch (error) {
        console.log("MediaREcording Error");
    }

    document.querySelector('#stopwatch').textContent = `${1}:${3}${0}`;
    resetStopwatch();
    document.querySelector('#status').textContent = 'Disconnected!! ,Press Record to transcribe again';
    document.querySelector('#accuracy').textContent = '0';
    document.querySelector('#latency').textContent = '0';
};