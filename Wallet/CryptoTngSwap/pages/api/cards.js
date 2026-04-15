import { state, supportedCards, addCard } from '../../lib/data';

export default function handler(req, res) {
  if (req.method === 'GET') {
    return res.status(200).json({ cards: state.cards, supportedCards });
  }

  if (req.method === 'POST') {
    try {
      const card = addCard(req.body);
      return res.status(200).json({ card });
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
