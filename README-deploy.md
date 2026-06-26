# Deploy

1. Copy project to VPS:
   ```bash
   rsync -av ~/projects/vizitka-bot/ marga@VPS_IP:/home/marga/projects/vizitka-bot/
   ```

2. On VPS — install deps:
   ```bash
   python3 -m venv ~/.venv
   ~/.venv/bin/pip install -r requirements.txt
   ```

3. Create .env on VPS:
   ```
   BOT_TOKEN=<token from BotFather>
   MARGA_CHAT_ID=<твой_chat_id>
   DB_PATH=vizitka_bot.db
   ```

4. Enable and start service:
   ```bash
   sudo cp vizitka-bot.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable vizitka-bot
   sudo systemctl start vizitka-bot
   sudo systemctl status vizitka-bot
   ```

5. Check logs:
   ```bash
   journalctl -u vizitka-bot -f
   ```

6. Update vizitka button URL in vizitka.html to t.me/MargaAstBrief_bot?start=vizitka
   (already done — button already points to the bot)
