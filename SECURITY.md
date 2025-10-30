# Security Guidelines

## 🔐 API Key Security

### ❌ Never Do This:
- Commit API keys to the repository
- Share API keys in issues or pull requests
- Include API keys in screenshots or documentation
- Store API keys in plain text files that might be committed

### ✅ Best Practices:

#### Local Development:
1. Copy `.env.example` to `.env`
2. Add your API key to `.env` (this file is gitignored)
3. Never commit the `.env` file

#### GitHub Actions:
1. Go to Repository Settings → Secrets and variables → Actions
2. Add `ANTHROPIC_API_KEY` as a repository secret
3. Use `${{ secrets.ANTHROPIC_API_KEY }}` in workflows

#### Production Deployment:
- Use environment variables or secure secret management
- Never hardcode API keys in application code
- Rotate API keys regularly

## 🚨 If You Accidentally Commit an API Key:

1. **Immediately revoke the key** at https://console.anthropic.com/
2. **Generate a new API key**
3. **Remove the key from git history**:
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all
   ```
4. **Force push** (⚠️ Warning: This rewrites history)
   ```bash
   git push origin --force --all
   ```

## 🔍 Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in committed files
- [ ] GitHub secrets configured for Actions
- [ ] API keys rotated regularly
- [ ] Access logs monitored

## 📞 Report Security Issues

If you discover a security vulnerability, please email [security@yourproject.com] instead of opening a public issue.