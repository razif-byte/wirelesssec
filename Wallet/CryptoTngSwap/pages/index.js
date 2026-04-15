import { useEffect, useMemo, useState } from 'react';

const formatMYR = (value) => `RM ${Number(value).toLocaleString('en-MY', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

export default function Home() {
  const [wallet, setWallet] = useState(null);
  const [cards, setCards] = useState([]);
  const [supportedCards, setSupportedCards] = useState([]);
  const [crypto, setCrypto] = useState({ balances: [], market: [] });
  const [topupAmount, setTopupAmount] = useState('50');
  const [cardForm, setCardForm] = useState({ type: 'Visa', name: '', number: '', expiry: '', cvv: '' });
  const [swapForm, setSwapForm] = useState({ fromToken: 'BTC', toToken: 'ETH', amount: '0.001' });
  const [message, setMessage] = useState('');
  const [swapMessage, setSwapMessage] = useState('');

  const totalCryptoValue = useMemo(() => {
    return crypto.balances.reduce((sum, item) => sum + (item.valueMYR || 0), 0);
  }, [crypto.balances]);

  useEffect(() => {
    refreshAll();
  }, []);

  async function refreshAll() {
    await Promise.all([loadWallet(), loadCards(), loadCrypto()]);
  }

  async function loadWallet() {
    const res = await fetch('/api/ewallet');
    const data = await res.json();
    setWallet(data);
  }

  async function loadCards() {
    const res = await fetch('/api/cards');
    const data = await res.json();
    setCards(data.cards || []);
    setSupportedCards(data.supportedCards || []);
  }

  async function loadCrypto() {
    const res = await fetch('/api/crypto');
    const data = await res.json();
    setCrypto(data);
  }

  async function handleTopup(event) {
    event.preventDefault();
    setMessage('');
    const res = await fetch('/api/ewallet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'topup', amount: Number(topupAmount) })
    });
    const data = await res.json();
    if (res.ok) {
      setWallet((prev) => ({ ...prev, balance: data.balance, transactions: [data.transaction, ...prev.transactions] }));
      setMessage(`Topup berjaya RM ${Number(topupAmount).toFixed(2)}`);
      setTopupAmount('50');
    } else {
      setMessage(data.error || 'Topup gagal');
    }
  }

  async function handleAddCard(event) {
    event.preventDefault();
    setMessage('');
    const res = await fetch('/api/cards', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cardForm)
    });
    const data = await res.json();
    if (res.ok) {
      setCards((prev) => [data.card, ...prev]);
      setMessage(`Kad ${data.card.type} berjaya ditambah`);
      setCardForm({ type: 'Visa', name: '', number: '', expiry: '', cvv: '' });
    } else {
      setMessage(data.error || 'Gagal tambah kad');
    }
  }

  async function handleSwap(event) {
    event.preventDefault();
    setSwapMessage('');
    const res = await fetch('/api/swap', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(swapForm)
    });
    const data = await res.json();
    if (res.ok) {
      setSwapMessage(`Swap berjaya: ${swapForm.amount} ${swapForm.fromToken} → ${data.swap.receivedAmount} ${swapForm.toToken}`);
      await loadCrypto();
    } else {
      setSwapMessage(data.error || 'Swap gagal');
    }
  }

  return (
    <main className="page-container">
      <header className="hero-card">
        <div>
          <p className="eyebrow">CryptoTngSwap</p>
          <h1>Dompet digital + Crypto Swap</h1>
          <p>Top-up eWallet, tambah kad Visa/Mastercard/Debit dan tukar token kripto dalam satu tempat.</p>
        </div>
      </header>

      <section className="grid-2">
        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">eWallet MYR</p>
              <h2>{wallet ? formatMYR(wallet.balance) : '...'}</h2>
            </div>
            <span className="badge">TNG-style</span>
          </div>

          <form className="card-form" onSubmit={handleTopup}>
            <label>
              Tambah nilai (MYR)
              <input
                value={topupAmount}
                onChange={(event) => setTopupAmount(event.target.value)}
                type="number"
                min="1"
                step="1"
                required
              />
            </label>
            <button type="submit">Top-up</button>
          </form>

          {message ? <p className="note">{message}</p> : null}

          <div className="transactions">
            <h3>Transaksi terakhir</h3>
            {wallet?.transactions?.length ? (
              <ul>
                {wallet.transactions.slice(0, 6).map((tx) => (
                  <li key={tx.id}>
                    <span>{tx.type}</span>
                    <span className={tx.amount < 0 ? 'negative' : 'positive'}>
                      {tx.amount < 0 ? '-' : '+'}{formatMYR(Math.abs(tx.amount))}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <p>Tiada transaksi</p>
            )}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Kad pembayaran</p>
              <h2>Visa / Mastercard / Debit</h2>
            </div>
            <span className="badge green">Tambah kad</span>
          </div>

          <form className="card-form" onSubmit={handleAddCard}>
            <label>
              Jenis kad
              <select value={cardForm.type} onChange={(event) => setCardForm({ ...cardForm, type: event.target.value })}>
                {supportedCards.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </label>
            <label>
              Nama pada kad
              <input
                value={cardForm.name}
                onChange={(event) => setCardForm({ ...cardForm, name: event.target.value })}
                type="text"
                placeholder="Nama penuh"
                required
              />
            </label>
            <label>
              Nombor kad
              <input
                value={cardForm.number}
                onChange={(event) => setCardForm({ ...cardForm, number: event.target.value })}
                type="text"
                placeholder="4111 1111 1111 1111"
                required
              />
            </label>
            <div className="two-col">
              <label>
                Luput
                <input
                  value={cardForm.expiry}
                  onChange={(event) => setCardForm({ ...cardForm, expiry: event.target.value })}
                  type="text"
                  placeholder="MM/YY"
                  required
                />
              </label>
              <label>
                CVV
                <input
                  value={cardForm.cvv}
                  onChange={(event) => setCardForm({ ...cardForm, cvv: event.target.value })}
                  type="password"
                  placeholder="123"
                  required
                />
              </label>
            </div>
            <button type="submit">Simpan kad</button>
          </form>

          <div className="cards-list">
            <h3>Kad anda</h3>
            {cards.length ? (
              <ul>
                {cards.map((card) => (
                  <li key={card.id}>
                    <div>
                      <strong>{card.type}</strong>
                      <span>{card.number}</span>
                    </div>
                    <div>
                      <small>{card.name}</small>
                      <small>{card.expiry}</small>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p>Belum ada kad</p>
            )}
          </div>
        </div>
      </section>

      <section className="panel crypto-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Crypto Wallet</p>
            <h2>Nilai portfolio: {formatMYR(totalCryptoValue)}</h2>
          </div>
          <span className="badge blue">Swap</span>
        </div>

        <div className="grid-2">
          <div>
            <h3>Portfolio kripto</h3>
            <table>
              <thead>
                <tr>
                  <th>Token</th>
                  <th>Jumlah</th>
                  <th>Harga</th>
                  <th>Nilai (MYR)</th>
                </tr>
              </thead>
              <tbody>
                {crypto.balances.map((item) => (
                  <tr key={item.symbol}>
                    <td>{item.symbol}</td>
                    <td>{item.amount}</td>
                    <td>{formatMYR(item.price)}</td>
                    <td>{formatMYR(item.valueMYR)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div>
            <h3>Tukar kripto</h3>
            <form className="card-form" onSubmit={handleSwap}>
              <label>
                Dari token
                <select value={swapForm.fromToken} onChange={(event) => setSwapForm({ ...swapForm, fromToken: event.target.value })}>
                  {crypto.market.map((item) => (
                    <option key={item.symbol} value={item.symbol}>{item.symbol}</option>
                  ))}
                </select>
              </label>
              <label>
                Kepada token
                <select value={swapForm.toToken} onChange={(event) => setSwapForm({ ...swapForm, toToken: event.target.value })}>
                  {crypto.market.map((item) => (
                    <option key={item.symbol} value={item.symbol}>{item.symbol}</option>
                  ))}
                </select>
              </label>
              <label>
                Jumlah dari
                <input
                  value={swapForm.amount}
                  onChange={(event) => setSwapForm({ ...swapForm, amount: event.target.value })}
                  type="number"
                  min="0.000001"
                  step="0.000001"
                  required
                />
              </label>
              <button type="submit">Tukar</button>
            </form>
            {swapMessage ? <p className="note">{swapMessage}</p> : null}
          </div>
        </div>
      </section>
    </main>
  );
}
