const ftp = require('basic-ftp');
const fs = require('fs');
const path = require('path');

async function deployToFTP() {
  const client = new ftp.Client();
  client.ftp.verbose = true;

  try {
    console.log('Connecting to FTP server...');
    await client.access({
      host: 'ftp.nasadef.com.my',
      user: 'razif@nasadef.com.my',
      password: 'Nikrazif@1',
      secure: false
    });

    console.log('Connected successfully!');

    // Navigate to the public_html directory first
    await client.cd('public_html');

    // Create aiapp directory if it doesn't exist
    try {
      await client.cd('aiapp');
      console.log('aiapp directory exists');
    } catch (error) {
      console.log('Creating aiapp directory...');
      await client.ensureDir('aiapp');
      await client.cd('aiapp');
    }

    // Upload files
    const filesToUpload = [
      'index.html',
      'app.js',
      'package.json',
      'package-lock.json'
    ];

    console.log('Uploading files...');
    for (const file of filesToUpload) {
      if (fs.existsSync(file)) {
        console.log(`Uploading ${file}...`);
        await client.uploadFrom(file, file);
      } else {
        console.log(`File ${file} not found, skipping...`);
      }
    }

    // Create a simple .htaccess file for proper routing
    const htaccess = `RewriteEngine On
RewriteRule ^$ /app.js [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /app.js [L]`;

    fs.writeFileSync('.htaccess', htaccess);
    await client.uploadFrom('.htaccess', '.htaccess');

    console.log('Deployment completed successfully!');
    console.log('Your app should be available at: https://aiapp.nasadef.com.my');

  } catch (error) {
    console.error('FTP deployment failed:', error);
  } finally {
    client.close();
  }
}

deployToFTP();