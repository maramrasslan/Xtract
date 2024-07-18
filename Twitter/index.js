const express = require('express');
const fs = require("fs");
const puppeteer = require("puppeteer");
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const session = require('express-session');
const bcrypt = require('bcrypt');
const User = require('./models/User.js');
const SearchHistory = require('./models/SearchHistory.js');
const Search = require('./models/search.js');
const authMiddleware = require('./middleware/auth');
const jwt = require('jsonwebtoken');
const helmet = require ("helmet");
require('dotenv').config();

// File paths using __dirname to ensure correct resolution
const COOKIES_PATH = path.join(__dirname, 'cookies.json');
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const JWT_SECRET = process.env.JWT_SECRET;
const SESSION_SECRET = process.env.SESSION_SECRET;
const MONGO_URI = process.env.MONGO_URI;

// Function to read credentials from file
async function readCredentials() {
    if (!fs.existsSync(CREDENTIALS_PATH)) {
        throw new Error('Credentials file not found');
    }
    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH));
    return credentials;
}

// Function to save cookies to file
async function saveCookies(page) {
    const cookies = await page.cookies();
    fs.writeFileSync(COOKIES_PATH, JSON.stringify(cookies, null, 2));
}

// Function to load cookies from file
async function loadCookies(page) {
    if (!fs.existsSync(COOKIES_PATH)) {
        return false;
    }
    const cookies = JSON.parse(fs.readFileSync(COOKIES_PATH));
    await page.setCookie(...cookies);
    await timeout(1000);
    return true;
}

// Function to perform login
async function login(page, email, password) {
    await page.goto('https://x.com/i/flow/login');

    // Fill in the login form
    await page.waitForSelector("[autocomplete=\"username\"]");
    await page.focus("[autocomplete=\"username\"]");
    await timeout(1000);
    await page.keyboard.type(email);
    await page.keyboard.press('Enter');
    await timeout(2000);
    await page.waitForSelector("[autocomplete=\"current-password\"]");
    await page.keyboard.type(password);
    await page.keyboard.press('Enter');

    // Wait for navigation to complete after login
    await page.waitForNavigation();

    // Save cookies after login
    await saveCookies(page);
}

// Function to check if the user is logged in
async function checkLogin(page) {
    await page.goto('https://x.com/home');
    await timeout(1000);
    // Check for a specific element that indicates successful login
    await page.waitForSelector('[data-testid=\"tweet\"] [data-testid=\"User-Name\"] ');
    const loggedIn = await page.evaluate(() => {
        return !!document.querySelector('[data-testid=\"tweet\"] [data-testid=\"User-Name\"] ');
    });
    return loggedIn;
}

//timeout function
function timeout(milliseconds) {
    return new Promise((resolve) => {
        setTimeout(() => { resolve() }, milliseconds);
    });
}

//object to csv function
function objectToCsv(data) {
    const csvRows = [];
    const headers = Object.keys(data[0]);
    csvRows.push(headers.join(','));
    for (const row of data) {
        const values = headers.map(header => `"${row[header]}"`);
        csvRows.push(values.join(','));
    }
    return csvRows.join('\n');
}

//extract profiles
async function extractProfile(page) {
    await timeout(1000);
    await page.evaluate(() => {
        window.scrollBy(0, 1000);
    });

    await timeout(2000);
    await page.waitForSelector('[data-testid=\"UserCell\"]');
    const profileLink = await page.evaluate(() => Array.from(
        document.querySelectorAll("[data-testid=\"UserCell\"] a[role=\"link\"]")
    ).map(profile => profile.href));

    await page.waitForSelector('[data-testid=\"UserCell\"] img');
    const profileImg = await page.evaluate(() => Array.from(
        document.querySelectorAll("[data-testid=\"UserCell\"] img")
    ).map(image => image.currentSrc));

    let profileLinkImg = [];
    for (let i = 0; i < profileLink.length; i++) {
        let obj = { ProfileLink: profileLink[i], ProfileImg: profileImg[i] };
        profileLinkImg.push(obj);
    }
    return profileLinkImg;
}

//extract date 
async function extractDate(page) {
    await timeout(1000);
    await page.waitForSelector('[data-testid=\"tweet\"] [data-testid=\"User-Name\"] ');
    const extractedDates = await page.evaluate(() => Array.from(
        document.querySelectorAll("[data-testid=\"tweet\"] [data-testid=\"User-Name\"] a[role=\"link\"] time[datetime]")
    ).map(element => element.dateTime));
    return extractedDates;
}

//extract tweet link and date
async function extractTlinkTdate(page) {
    await timeout(1000);
    await page.evaluate(() => {
        window.scrollBy(0, 1000);
    });
    //extract all 3 links
    await timeout(1000);
    await page.waitForSelector('[data-testid=\"tweet\"] [data-testid=\"User-Name\"]');
    const extractedLINKS = await page.evaluate(() => Array.from(
        document.querySelectorAll("[data-testid=\"tweet\"] [data-testid=\"User-Name\"] a[role=\"link\"]")
    ).map(tweet => tweet.href));
    //extract only the third link to get the tweet link
    let extractedLinks = [];
    for (let i = 2; i < extractedLINKS.length; i = i + 3) {
        extractedLinks.push(extractedLINKS[i]);
    }
    //add date and link to array of objects
    const extractedDates = await extractDate(page);
    let linkDateList = [];
    for (let i = 0; i < extractedLinks.length; i++) {
        let obj = { TweetLink: extractedLinks[i], TweetDate: extractedDates[i] };
        linkDateList.push(obj);
    }
    return linkDateList;
}

//extract tweet text date and link
async function extractItems(page) {
    await timeout(1000);
    const resultDateLink = await extractTlinkTdate(page);
    await page.waitForSelector('[data-testid=\"tweetText\"]');
    const extractedItemsText = await page.evaluate(() => Array.from(
        document.querySelectorAll("[data-testid=\"tweetText\"]")
    ).map(element => element.innerText));
    //add text to the objects 
    let extractedTweets = [];
    for (let i = 0; i < resultDateLink.length; i++) {
        let newObj = {
            TweetLink: resultDateLink[i].TweetLink,
            TweetDate: resultDateLink[i].TweetDate,
            TweetText: extractedItemsText[i]
        };
        extractedTweets.push(newObj);
    }

    return extractedTweets;
}

async function findProfile(page, profileName) {
    try {
        const url = `https://x.com/search?q=${encodeURIComponent(profileName)}&src=typed_query&f=user`;
        let output = [];
        page.goto(url);
        await timeout(1000);
        await page.waitForNavigation();

        loopLimit = 30; //find max 30 profiles
        while (output.length < loopLimit) {
            await timeout(2000);
            resultProfiles = await extractProfile(page);
            for (const profile of resultProfiles) {
                let twitterLink = false;
                let link = (profile.ProfileLink).toLowerCase();
                if (link.indexOf("https://twitter.com/") > -1 || link.indexOf("https://x.com/") > -1) {
                    twitterLink = true;
                }
                let index = output.findIndex((item) => item.ProfileLink === profile.ProfileLink);
                if (index === -1 && output.length < loopLimit && twitterLink == true) {
                    output.push(profile);
                }
            }
        }
        return output;
    } catch (err) {
        console.error(err);
    }
}

//Function that executes if we search by profile
async function SearchByProfile(page, username, loopLimit, keyword, startDate, endDate, startTime, endTime) {
    try {
        //setup profile page 
        const url = `https://twitter.com/${username}`;
        await page.goto(url);
        await timeout(3000);
        //const and vars 
        const defaultLimit = 10;
        let resultTweet = [];
        let output = [];
        let foundKeyword = false;
        let foundDate = false;
        let foundTime = false;
        if (loopLimit == null) { loopLimit = defaultLimit; }

        while (output.length < loopLimit) {
            await timeout(2000);
            resultTweet = await extractItems(page);
            for (const tweet of resultTweet) {
                if ((tweet.TweetText) != null) {
                    let index = output.findIndex((item) => item.TweetLink === tweet.TweetLink);
                    //logic to find the keyword in the text
                    let tweettextclean = (tweet.TweetText).replace(/[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi, '');
                    let tweettext = tweettextclean.toLowerCase();

                    keyword = keyword.toLowerCase();
                    if ((tweettext.indexOf(keyword)) >= 0 || keyword == "") {
                        foundKeyword = true;
                    } else { foundKeyword = false; }
                    //logic to test the date filter
                    let date = new Date(tweet.TweetDate);
                    if (startDate != "" || endDate != "") {
                        startDate = new Date(startDate);
                        endDate = new Date(endDate);
                        if (date >= startDate && date <= endDate) {
                            foundDate = true;
                        } else { foundDate = false; }
                    } else { foundDate = true; }
                    //logic to test time filter
                    if (startTime != "" || endTime != "") {
                        const hours = date.getUTCHours();
                        const minutes = date.getUTCMinutes();
                        const seconds = date.getUTCSeconds();
                        const extractedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
                        const today = new Date().toISOString().slice(0, 10);
                        const startTimeObj = new Date(`${today}T${startTime}Z`);
                        const endTimeObj = new Date(`${today}T${endTime}Z`);
                        console.log(startTimeObj, endTimeObj);
                        const extractedTimeObj = new Date(`${today}T${extractedTime}Z`);
                        if (extractedTimeObj >= startTimeObj && extractedTimeObj <= endTimeObj) {
                            foundTime = true;
                            if(extractedTimeObj < startTimeObj){foundTime=false; break;}
                        } else { foundTime = false; }
                    } else { foundTime = true; }
                    //check if all filters apply to the tweet then add it 
                    if (index === -1 && output.length < loopLimit && foundKeyword == true && foundDate == true && foundTime == true) {
                        output.push(tweet);
                    }
                }
            }
        }
        const slicedOutput = output.slice(0, loopLimit);
        console.log(slicedOutput);
        const csvData = objectToCsv(slicedOutput);
        fs.writeFile("profile_output.csv", csvData, function (err) {
            if (err) throw err;
            console.log('write to profile csv file complete');
        });
        console.log(output.length);
        return output;

    } catch (err) {
        console.error(err);
    }
}

//Function that executes if we search by keyword
async function SearchByKeyword(page, keyword, loopLimit, startDate, endDate, startTime, endTime) {
    try {
        await page.goto(`https://twitter.com/search?q=${encodeURIComponent(keyword)}&src=typed_query`);
        await timeout(2000);

        const defaultLimit = 10;
        let resultTweet = [];
        let output = [];
        let foundKeyword = false;
        let foundDate = false;
        let foundTime = false;
        if (loopLimit == null) { loopLimit = defaultLimit; }

        while (output.length < loopLimit) {
            await timeout(2000);
            resultTweet = await extractItems(page);
            for (const tweet of resultTweet) {
                if ((tweet.TweetText) != null) {
                    let index = output.findIndex((item) => item.TweetLink === tweet.TweetLink);
                    //logic to find the keyword in the text
                    let tweettextclean = (tweet.TweetText).replace(/[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi, '');
                    let tweettext = tweettextclean.toLowerCase();

                    keyword = keyword.toLowerCase();
                    if ((tweettext.indexOf(keyword)) >= 0 || keyword == "") {
                        foundKeyword = true;
                    } else { foundKeyword = false; }
                    //logic to test the date filter
                    let date = new Date(tweet.TweetDate);
                    if (startDate != "" || endDate != "") {
                        startDate = new Date(startDate);
                        endDate = new Date(endDate);
                        if (date >= startDate && date <= endDate) {
                            foundDate = true;
                        } else { foundDate = false; }
                    } else { foundDate = true; }
                    //logic to test time filter
                    if (startTime != "" || endTime != "") {
                        const hours = date.getUTCHours();
                        const minutes = date.getUTCMinutes();
                        const seconds = date.getUTCSeconds();
                        const extractedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
                        const today = new Date().toISOString().slice(0, 10);
                        const startTimeObj = new Date(`${today}T${startTime}Z`);
                        const endTimeObj = new Date(`${today}T${endTime}Z`);
                        const extractedTimeObj = new Date(`${today}T${extractedTime}Z`);
                        if (extractedTimeObj >= startTimeObj && extractedTimeObj <= endTimeObj) {
                            foundTime = true;
                        } else { foundTime = false; }
                    } else { foundTime = true; }
                    //check if all filters apply to the tweet then add it 
                    if (index === -1 && output.length < loopLimit && foundDate == true && foundTime == true && foundKeyword == true) {
                        output.push(tweet);
                    }
                }
            }
        }
        const slicedOutput = output.slice(0, loopLimit);
        console.log(slicedOutput);
        const csvData = objectToCsv(slicedOutput);
        fs.writeFile("keyword_output.csv", csvData, function (err) {
            if (err) throw err;
            console.log('write to keyword csv file complete');
        });
        console.log(output.length);
        return output;
    } catch (err) {
        console.error(err);
    }
}

// Create an Express app
const app = express();
const port = 3000;

app.use(cors());
app.use(helmet());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(session({
    secret: SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
}));

// MongoDB connection
mongoose.connect(MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    dbName: 'App',
}).then(() => {
    console.log('Connected to MongoDB');
}).catch(err => {
    console.error('Error connecting to MongoDB:', err);
    process.exit(1); // Exit the process if unable to connect to MongoDB
});

// Routes
//Signup
app.post('/signup', async (req, res) => {
    try {
        const { username, password } = req.body;
        const existingUser = await User.findOne({ username });
        if (existingUser) {
            return res.status(400).json({ message: 'User already exists' });
        }
        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = new User({ username, password: hashedPassword });
        await newUser.save();
        req.session.userId = newUser._id;
        res.json({ message: 'User created successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

//Login
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const user = await User.findOne({ username });
        if (!user || !await bcrypt.compare(password, user.password)) {
            return res.status(401).json({ message: 'Invalid username or password' });
        }

        const token = jwt.sign({ userId: user._id }, JWT_SECRET, { expiresIn: '18h' });

        res.json({ message: 'Login successful', token });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

//Profile
app.get('/profile', authMiddleware, async (req, res) => {
    try {
        const user = await User.findById(req.userId).select('-password');
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.json(user);
    } catch (error) {
        console.error('Profile retrieval error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

//change password
app.post('/change-password', authMiddleware, async (req, res) => {
    const { currentPassword, newPassword } = req.body;

    try {
        // Find the user by ID
        const user = await User.findById(req.userId);
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        // Check if the current password is correct
        const isMatch = await bcrypt.compare(currentPassword, user.password);
        if (!isMatch) {
            return res.status(400).json({ message: 'Current password is incorrect' });
        }

        // Hash the new password
        const salt = await bcrypt.genSalt(10);
        user.password = await bcrypt.hash(newPassword, salt);

        // Save the updated user
        await user.save();

        res.json({ message: 'Password changed successfully' });
    } catch (error) {
        console.error('Password change error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

//Logout
app.post('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            return res.status(500).json({ message: 'Logout failed' });
        }
        res.clearCookie('connect.sid');
        res.json({ message: 'Logout successful' });
    });
});

//History
app.get('/history', authMiddleware, async (req, res) => {
    try {
        const searchHistory = await SearchHistory.find({ userId: req.userId });
        if (!searchHistory) {
            return res.status(404).json({ message: 'No search history found' });
        }
        res.json(searchHistory);
    } catch (error) {
        console.error('History retrieval error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

//find profiles api
app.post('/findProfile', authMiddleware, async (req, res) => {
    const { profileName } = req.body;
    const searchStartTime = Date.now();

    try {
        const browser = await puppeteer.launch({ headless: true });
        var page = await browser.newPage();

        // Log in
        const cookiesLoaded = await loadCookies(page);
        await timeout(1000);
        if (cookiesLoaded) {
            const isLoggedIn = await checkLogin(page);
            if (!isLoggedIn) {
                // Read credentials from file
                const credentials = await readCredentials();
                const { email, password } = credentials;
                // Perform login
                await login(page, email, password);
            }
        } else {
            const credentials = await readCredentials();
            const { email, password } = credentials;
            await login(page, email, password);
        }

        await timeout(1000);
        results = await findProfile(page, profileName);
        await browser.close();

        const searchEndTime = Date.now();
        const duration = searchEndTime - searchStartTime;

        //save in search table
        if (req.userId) {
            const search = new Search({
                userId: req.userId,
                query: profileName,
                duration,
            });
            await search.save();
        }

        // Save search history if user is logged in
        if (req.userId) {
            const searchHistory = new SearchHistory({
                query: profileName,
                userId: req.userId,
            });
            await searchHistory.save();
        }

        res.json({ results });

    } catch (err) {
        console.error('Error during Profile search:', err);
        res.status(500).send('An error occurred during profile search.');
    }

});

//statistics routes
app.get('/statistics/total-searches', authMiddleware, async (req, res) => {
    try {
        const totalSearches = await Search.countDocuments();
        res.json({ totalSearches });
    } catch (error) {
        console.error('Total searches error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

app.get('/statistics/searches-per-user', authMiddleware, async (req, res) => {
    try {
        const searchesPerUser = await Search.aggregate([
            { $group: { _id: '$userId', count: { $sum: 1 } } }
        ]);
        res.json(searchesPerUser);
    } catch (error) {
        console.error('Searches per user error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

app.get('/statistics/searches-over-time', authMiddleware, async (req, res) => {
    try {
        const searchesOverTime = await Search.aggregate([
            {
                $addFields: {
                    createdAtDate: {
                        $convert: {
                            input: "$createdAt",
                            to: "date",
                            onError: null,  // Handle conversion errors
                            onNull: null    // Handle null values
                        }
                    }
                }
            },
            {
                $group: {
                    _id: { $dateToString: { format: "%Y-%m-%d", date: "$createdAtDate" } },
                    count: { $sum: 1 }
                }
            },
            { $sort: { _id: 1 } }
        ]);
        res.json(searchesOverTime);
    } catch (error) {
        console.error('Searches over time error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});


app.get('/statistics/average-search-duration', authMiddleware, async (req, res) => {
    try {
        const averageSearchDuration = await Search.aggregate([
            {
                $group: {
                    _id: null,
                    avgDuration: { $avg: "$duration" }
                }
            }
        ]);
        res.json(averageSearchDuration[0]);
    } catch (error) {
        console.error('Average search duration error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

app.get('/statistics/user-searches-over-time', authMiddleware, async (req, res) => {
    try {
        const userId = new mongoose.Types.ObjectId(req.userId); // Ensure `userId` is an ObjectId
        const userSearchesOverTime = await Search.aggregate([
            { $match: { userId } }, // Match searches for the current user
            {
                $addFields: {
                    createdAtDate: {
                        $convert: {
                            input: "$createdAt",
                            to: "date",
                            onError: null,
                            onNull: null
                        }
                    }
                }
            },
            {
                $group: {
                    _id: { $dateToString: { format: "%Y-%m-%d", date: "$createdAtDate" } },
                    count: { $sum: 1 }
                }
            },
            { $sort: { _id: 1 } } // Sort by date ascending
        ]);
        res.json(userSearchesOverTime);
    } catch (error) {
        console.error('User searches over time error:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});


// Directory where the files will be saved
const downloadDirectory = path.join(__dirname, 'downloads');

// Ensure the directory exists
if (!fs.existsSync(downloadDirectory)) {
    fs.mkdirSync(downloadDirectory);
}

// Define a route to handle the search
app.post('/search', authMiddleware, async (req, res) => {
    const { searchMethod, username, keyword, loopLimit, startDate, endDate, startTime, endTime } = req.body;
    const searchStartTime = Date.now();

    try {
        const browser = await puppeteer.launch({ headless: true });
        var page = await browser.newPage();

        let output = [];
        // Log in
        const cookiesLoaded = await loadCookies(page);
        await timeout(1000);
        if (cookiesLoaded) {
            const isLoggedIn = await checkLogin(page);
            if (!isLoggedIn) {
                // Read credentials from file
                const credentials = await readCredentials();
                const { email, password } = credentials;
                // Perform login
                await login(page, email, password);
            }
        } else {
            const credentials = await readCredentials();
            const { email, password } = credentials;
            await login(page, email, password);
        }

        await timeout(2000);
        switch (searchMethod) {
            case "Search in user profile":
                output = await SearchByProfile(page, username, loopLimit, keyword, startDate, endDate, startTime, endTime);
                break;
            case "Search by keyword":
                output = await SearchByKeyword(page, keyword, loopLimit, startDate, endDate, startTime, endTime);
                break;
            default:
                res.status(400).send('Invalid search method.');
                return; // Exit the function early
        }
        await browser.close();

        const searchEndTime = Date.now();
        const duration = searchEndTime - searchStartTime;

        //save in search table
        if (req.userId) {
            const search = new Search({
                userId: req.userId,
                query: username || keyword,
                duration,
            });
            await search.save();
        }
        // Save search history if user is logged in
        if (req.userId) {
            const searchHistory = new SearchHistory({
                query: username || keyword,
                userId: req.userId,
            });
            await searchHistory.save();
        }
        const fileName = 'results';
        const csvData = objectToCsv(output);
        const jsonFilePath = path.join(downloadDirectory, `${fileName}.json`);
        const csvFilePath = path.join(downloadDirectory, `${fileName}.csv`);

        fs.writeFileSync(jsonFilePath, JSON.stringify(output, null, 2));
        fs.writeFileSync(csvFilePath, csvData);

        results = output;
        res.json({ results, fileName });

    } catch (err) {
        console.error('Error during search:', err);
        res.status(500).send('An error occurred during the search.');
    }
});

// Serve the CSV and JSON files for download
app.get('/download/:fileName', (req, res) => {
    const { fileName } = req.params;
    const fileFormat = req.query.fileFormat;

    const filePath = path.join(downloadDirectory, `${fileName}.${fileFormat}`);

    if (fs.existsSync(filePath)) {
        res.download(filePath);
    } else {
        res.status(404).send('File not found');
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
/* Important 
*notification pop up selector data-testid="app-bar-close" 
*need to see if it pops up to close it as it blocks the normal 
*functioning of the page */