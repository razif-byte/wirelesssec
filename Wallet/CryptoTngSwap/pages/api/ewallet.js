import { state, topUp } from '../../lib/data';

export default function handler(req, res) {
  if (req.method === 'GET') {
    return res.status(200).json({
      balance: state.ewallet.balance,
      currency: state.ewallet.currency,
      transactions: state.ewallet.transactions
    });
  }

  if (req.method === 'POST') {
    const { action, amount } = req.body;
    if (action === 'topup') {
      try {
        const topup = topUp(Number(amount));
        return res.status(200).json({ balance: state.ewallet.balance, transaction: topup });
      } catch (error) {
        return res.status(400).json({ error: error.message });
      }
    }

    return res.status(400).json({ error: 'Action tidak disokong' });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
