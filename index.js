const admin = require('firebase-admin');
const axios = require('axios');
const cheerio = require('cheerio');

const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
}

const db = admin.firestore();

async function get2DLive() {
    try {
        const { data } = await axios.get('https://www.set.or.th/en/home', {
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });
        const $ = cheerio.load(data);

        const setIndexText = $(".set-index-value").first().text().trim();
        const valueText = $(".market-value").first().text().trim();

        if (setIndexText && valueText) {
            const lastDigitSet = setIndexText.slice(-1); 
            const integerPart = valueText.split('.')[0]; 
            const lastDigitValue = integerPart.slice(-1);
            const final2D = lastDigitSet + lastDigitValue;

            await db.collection('live_data').doc('current').set({
                set: setIndexText,
                value: valueText,
                result: final2D,
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            console.log(`Updated: ${final2D} at ${new Date().toLocaleTimeString()}`);
        }
    } catch (error) {
        console.error("Error fetching data:", error.message);
    }
}

// ၃ စက္ကန့်တစ်ကြိမ် ပတ်မည့် Function
async function startLoop() {
    // ၁ မိနစ်အတွင်း အကြိမ် ၂၀ ပတ်မည် (၂၀ x ၃ စက္ကန့် = ၆၀ စက္ကန့်)
    for (let i = 0; i < 20; i++) {
        await get2DLive();
        await new Promise(resolve => setTimeout(resolve, 3000)); 
    }
}

startLoop();
