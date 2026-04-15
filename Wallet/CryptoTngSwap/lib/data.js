const supportedCards = [
  'Visa',
  'Mastercard',
  'Debit Card',
  'Amex',
  'JCB',
  'UnionPay'
];

const cryptoPrices = {
  BTC: 120000.0,
  ETH: 8500.0,
  USDT: 4.6,
  BNB: 1350.0,
  SOL: 450.0
};

const state = {
  ewallet: {
    balance: 240.75,
    currency: 'MYR',
    transactions: [
      { id: 'tx3', type: 'Topup', amount: 120.0, date: '2026-04-14T19:00:00Z' },
      { id: 'tx2', type: 'Transfer', amount: -40.5, date: '2026-04-13T14:22:00Z' },
      { id: 'tx1', type: 'Merchant', amount: -18.0, date: '2026-04-12T09:05:00Z' }
    ]
  },
  cards: [
    {
      id: 'card-1',
      type: 'Visa',
      name: 'Razif Ahmad',
      number: '4111 1111 1111 1111',
      expiry: '12/28'
    }
  ],
  crypto: {
    balances: {
      BTC: 0.005,
      ETH: 0.14,
      USDT: 240.0,
      BNB: 1.2,
      SOL: 3.5
    },
    prices: cryptoPrices
  }
};

function formatId(prefix) {
  return `${prefix}-${Math.random().toString(36).slice(2, 10)}`;
}

function getMarket() {
  return Object.entries(state.crypto.prices).map(([symbol, price]) => ({ symbol, price }));
}

function addEwalletTransaction(type, amount) {
  const transaction = {
    id: formatId('tx'),
    type,
    amount,
    date: new Date().toISOString()
  };
  state.ewallet.transactions.unshift(transaction);
  if (state.ewallet.transactions.length > 12) {
    state.ewallet.transactions.pop();
  }
  return transaction;
}

function topUp(amount) {
  if (amount <= 0 || Number.isNaN(amount)) {
    throw new Error('Invalid top-up amount');
  }
  state.ewallet.balance += amount;
  return addEwalletTransaction('Topup', amount);
}

function addCard(card) {
  if (!card.type || !card.name || !card.number || !card.expiry) {
    throw new Error('Missing card data');
  }
  const normalized = {
    id: formatId('card'),
    type: supportedCards.includes(card.type) ? card.type : 'Debit Card',
    name: card.name.trim(),
    number: card.number.replace(/[^0-9]/g, '').replace(/(.{4})/g, '$1 ').trim(),
    expiry: card.expiry.trim()
  };
  state.cards.unshift(normalized);
  return normalized;
}

function getPrice(symbol) {
  if (!(symbol in state.crypto.prices)) {
    throw new Error('Unsupported crypto symbol');
  }
  return state.crypto.prices[symbol];
}

function swapCrypto(from, to, amount) {
  if (!(from in state.crypto.balances) || !(to in state.crypto.balances)) {
    throw new Error('Unsupported crypto token');
  }
  amount = Number(amount);
  if (amount <= 0 || Number.isNaN(amount)) {
    throw new Error('Invalid swap amount');
  }
  if (state.crypto.balances[from] < amount) {
    throw new Error('Insufficient wallet balance');
  }
  const fromPrice = getPrice(from);
  const toPrice = getPrice(to);
  const valueMYR = amount * fromPrice;
  const receivedAmount = Number((valueMYR / toPrice).toFixed(8));
  state.crypto.balances[from] = Number((state.crypto.balances[from] - amount).toFixed(8));
  state.crypto.balances[to] = Number((state.crypto.balances[to] + receivedAmount).toFixed(8));
  return {
    from,
    to,
    amount,
    receivedAmount,
    rate: Number((fromPrice / toPrice).toFixed(6)),
    valueMYR: Number(valueMYR.toFixed(2))
  };
}

export { state, supportedCards, getMarket, topUp, addCard, swapCrypto };
