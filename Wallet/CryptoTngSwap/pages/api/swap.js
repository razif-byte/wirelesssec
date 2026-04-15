import { state, swapCrypto } from '../../lib/data';

export default function handler(req, res) {
  if (req.method === 'POST') {
    const { fromToken, toToken, amount } = req.body;
    try {
      const swap = swapCrypto(fromToken, toToken, Number(amount));
      return res.status(200).json({ swap, balances: state.crypto.balances });
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  }
  return res.status(405).json({ error: 'Method not allowed' });
}
