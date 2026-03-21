const { execSync } = require('child_process');

/**
 * Compiles Tailwind v4 utilities to static/css/built.css.
 * Entry: static/css/tailwind.css (@import "tailwindcss" + dark variant for [data-theme="dark"]).
 * App styles: static/css/main.css (@imports built.css + tokens + components).
 */
console.log('Building Tailwind CSS (tailwind.css → built.css)...');

try {
  execSync('npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/built.css --minify', {
    stdio: 'inherit',
    cwd: __dirname
  });
  console.log('built.css updated. Use main.css in templates (no CDN).');
} catch (error) {
  console.error('Build failed:', error.message);
  process.exit(1);
}