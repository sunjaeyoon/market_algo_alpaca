const Alpaca = require('@alpacahq/alpaca-trade-api');
require('dotenv').config();

//process.env.{variable}

const alpaca = new Alpaca({
    keyId: process.env.keyId,
    secretKey: process.env.secretKey,
    paper: true,
})


alpaca.getAccount().then((account) => {
    console.log('Current Account:', account)
})

var getBar = async () =>{ 
    let resp = alpaca.getBarsV2(
        "AAPL",
        {
            start: "2021-02-01",
            end: "2021-02-10",
            limit: 2,
            timeframe: "1Day",
            adjustment: "all",
        },
        alpaca.configuration
    );
    const bars = [];

    for await (let b of resp) {
        console.log(b)
    }
}

getBar();