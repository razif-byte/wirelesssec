import { state, getMarket } from '../../lib/data';

export default function handler(req, res) {
  if (req.method === 'GET') {
    const balances = Object.entries(state.crypto.balances).map(([symbol, amount]) => ({
      symbol,
      amount,
      price: state.crypto.prices[symbol],
      valueMYR: Number((amount * state.crypto.prices[symbol]).toFixed(2))
    }));
    return res.status(200).json({ balances, market: getMarket() });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
