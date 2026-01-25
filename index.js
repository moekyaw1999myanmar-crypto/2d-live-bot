const admin = require('firebase-admin');
const axios = require('axios');

const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
}

const db = admin.firestore();

async function get2DLive() {
    try {
        const response = await axios.get('https://api.thaistock2d.com/live');
        const liveData = response.data.live;

        if (liveData) {
            const setIndex = liveData.set;
            const value = liveData.value;
            const result2D = liveData.twod;
            const time = liveData.time;

            await db.collection('live_data').doc('current').set({
                set: setIndex,
                value: value,
                result: result2D,
                live_time: time,
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });

            console.log(`SET: ${setIndex} | VAL: ${value} | 2D: ${result2D} | ${time}`);
        }
    } catch (error) {
        console.error("Error:", error.message);
    }
}

async function startLoop() {
    for (let i = 0; i < 20; i++) {
        await get2DLive();
        await new Promise(resolve => setTimeout(resolve, 3000));
    }
}

startLoop();
