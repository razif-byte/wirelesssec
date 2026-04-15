# CryptoTngSwap

A simple Next.js eWallet and crypto wallet demo with swap and card management.

## Features

- eWallet balance and top-up
- Add debit cards, Visa, Mastercard, and other card types
- Crypto wallet balances and market prices
- Cryptocurrency swap between supported tokens

## Run locally

1. Install dependencies:

```bash
npm install
```

2. Start development server:

```bash
npm run dev
```

3. Open the app:

http://localhost:3000

## Portable HTML Version

A self-contained HTML version is available at `index.html` that can run entirely offline in any modern web browser.

### Features of Portable Version:
- ✅ Complete wallet functionality
- ✅ Local storage for data persistence
- ✅ No server dependencies
- ✅ Works offline
- ✅ Responsive design
- ✅ Dark mode support
- ✅ All original features included

### How to Use Portable Version:
1. Open `index.html` in any modern web browser
2. Click "Sign in with Google" (simulated login)
3. Start using the wallet immediately
4. All data is stored locally in your browser

### Portable Version Limitations:
- Simulated authentication (no real Google login)
- No real-time price updates (uses fixed prices)
- No backend API calls (all operations are local)
- Data persists only in browser localStorage

The portable version is perfect for:
- Demonstrations
- Offline use
- Development testing
- Quick prototyping
- Educational purposes

## Deployment to aiapp.nasadef.com.my

The application is automatically deployed to https://aiapp.nasadef.com.my

### Auto Deployment Setup:
- **Server**: ftp.nasadef.com.my
- **User**: razif@nasadef.com.my
- **Path**: /public_html/aiapp/
- **Format**: Node.js app (app.js)

### Manual Deployment:
```bash
# Install dependencies
npm install

# Run deployment script
node deploy.js
```

### Files Deployed:
- `index.html` - Portable wallet application
- `app.js` - Node.js server
- `package.json` - Dependencies
- `.htaccess` - Apache configuration

The app should be available at: https://aiapp.nasadef.com.my
