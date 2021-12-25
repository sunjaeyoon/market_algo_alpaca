const Alpaca = require("@alpacahq/alpaca-trade-api");
require('dotenv').config();

class DataStream {
  constructor({ apiKey, secretKey, feed }) {
    this.alpaca = new Alpaca({
      keyId: apiKey,
      secretKey,
      feed,
    });

    const socket = this.alpaca.data_stream_v2;
    socket.onConnect(function () {
      console.log("15 Connected");
      socket.subscribeForQuotes(["AAPL"]);
      socket.subscribeForQuotes(["FB"]);
      socket.subscribeForTrades(["FB"]);
      socket.subscribeForBars(["SPY"]);
      socket.subscribeForStatuses(["*"]);
    });

    socket.onError((err) => {
      console.log(err);
    });

    socket.onStockTrade((trade) => {
      console.log("27")
      console.log(trade);
    });

    socket.onStockQuote((quote) => {
      console.log("31")
      console.log(quote);
    });

    socket.onStockBar((bar) => {
      console.log(bar);
    });

    socket.onStatuses((s) => {
      console.log("39 "+s);
    });

    socket.onStateChange((state) => {
      console.log(state);
    });

    socket.onDisconnect(() => {
      console.log("47 Disconnected");
    });

    socket.connect();

    // unsubscribe from FB after a second
    setTimeout(() => {
      //socket.unsubscribeFromTrades(["FB"]);
    }, 1000);
  }
}

let stream = new DataStream({
  apiKey: process.env.keyId,
  secretKey: process.env.secretKey,
  feed: "iex",
  paper: true,
});

