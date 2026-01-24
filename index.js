const admin = require('firebase-admin');
const axios = require('axios');
const cheerio = require('cheerio');

if (!process.env.FIREBASE_SERVICE_ACCOUNT) {
    console.error("Error: FIREBASE_SERVICE_ACCOUNT is missing!");
    process.exit(1);
}

const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
}

const db = admin.firestore();

async function get2DLive() {
    try {
        console.log("Fetching data from SET...");
        const { data } = await axios.get('https://www.set.or.th/en/home', {
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });
        const $ = cheerio.load(data);

        const setIndexText = $(".set-index-value").first().text().trim();
        const valueText = $(".market-value").first().text().trim();

        console.log(`Scraped Data: SET ${setIndexText}, Value ${valueText}`);

        if (setIndexText && valueText) {
            const lastDigitSet = setIndexText.slice(-1); 
            const integerPart = valueText.split('.')[0]; 
            const lastDigitValue = integerPart.slice(-1);
            const final2D = lastDigitSet + lastDigitValue;

            console.log(`Calculated 2D: ${final2D}`);

            await db.collection('live_data').doc('current').set({
                set: setIndexText,
                value: valueText,
                result: final2D,
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            console.log("Successfully saved to Firestore!");
        } else {
            console.error("Error: Could not find SET data on website.");
        }
    } catch (error) {
        console.error("Main Error:", error.message);
        process.exit(1);
    }
}

get2DLive();
