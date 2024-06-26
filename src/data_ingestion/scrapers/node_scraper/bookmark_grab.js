
let tweets = []; // Initialize an empty array to hold all tweet elements

const scrollInterval = 1000; 
const scrollStep = 5000; // Pixels to scroll on each step

let previousTweetCount = 0;
let unchangedCount = 0;

const scrollToEndIntervalID = setInterval(() => {
    window.scrollBy(0, scrollStep);
    const currentTweetCount = tweets.length;
    if (currentTweetCount === previousTweetCount) {
        unchangedCount++;
        if (unchangedCount >= 2) { // Stop if the count has not changed 5 times
            console.log('Scraping complete');
            console.log('Total tweets scraped: ', tweets.length);
            console.log('Downloading tweets as JSON...');
            clearInterval(scrollToEndIntervalID); // Stop scrolling
            observer.disconnect(); // Stop observing DOM changes
            downloadTweetsAsJson(tweets); // Download the tweets list as a JSON file
        }
    } else {
        unchangedCount = 0; // Reset counter if new tweets were added
    }
    previousTweetCount = currentTweetCount; // Update previous count for the next check
}, scrollInterval);


function updateTweets() {
    document.querySelectorAll('article[data-testid="tweet"]').forEach(tweetElement => {
        const authorName = tweetElement.querySelector('[data-testid="User-Name"]').innerText;
        const handle = tweetElement.querySelector('[role="link"]').href.split('/').pop();
        const tweetText = tweetElement.querySelector('[data-testid="tweetText"]').innerText;
        const time = tweetElement.querySelector('time').getAttribute('datetime');
        const link = tweetElement.querySelector('a[href*="/status/"]').href;
        
        const isTweetNew = !tweets.some(tweet => tweet.text === tweetText);
        if (isTweetNew) {
            tweets.push({
                authorName,
                handle,
                tweetText,
                time,
                link
            });
            console.log("tweets scraped: ", tweets.length);
        }
    });
}

// Initially populate the tweets array
updateTweets();

// Create a MutationObserver to observe changes in the DOM
const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        if (mutation.addedNodes.length) {
            updateTweets(); // Call updateTweets whenever new nodes are added to the DOM
        }
    });
});

// Start observing the document body for child list changes
observer.observe(document.body, { childList: true, subtree: true });

function downloadTweetsAsJson(tweetsArray) {
    const jsonData = JSON.stringify(tweetsArray); // Convert the array to JSON
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'tweets.json'; // Specify the file name
    document.body.appendChild(link); // Append the link to the document
    link.click(); // Programmatically click the link to trigger the download
    document.body.removeChild(link); // Clean up and remove the link
}