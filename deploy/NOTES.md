# NGINX configurations  for one template file HTML/CSS/JS
### works 100%
```nginx
server {  # Fix "erver" → "server"
    listen 80;
    server_name 54.166.6.159;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```
# NGINX configurations  for one statics file HTML/CSS/JS serrated
### works 20% serve just html
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }

    # Pass requests to the Django app (via Gunicorn or uWSGI)
    location / {
        proxy_pass http://127.0.0.1:8000;  # Change this to your Gunicorn or uWSGI server address
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
==================================================================
# To run a process on a remote server via SSH and keep it running even after you close the terminal, you can use one of the following options:

---

### ✅ Option 1: Use `nohup` (most common & simple)

```bash
nohup python your_script.py > output.log 2>&1 &
```

* `nohup` prevents the process from being killed when you log out.
* `> output.log 2>&1` redirects stdout and stderr to a file.
* `&` runs it in the background.

📝 You can later check the output with:

```bash
tail -f output.log
```

---

### ✅ Option 2: Use `tmux` (better for managing long-running tasks)

1. Start a tmux session:

```bash
tmux new -s mysession
```

2. Run your command:

```bash
python your_script.py
```

3. Detach from the session (leave it running):

```bash
Ctrl + B, then press D
```

4. Reattach later:

```bash
tmux attach -t mysession
```

5. Kill the session when done:

```bash
tmux kill-session -t mysession
```

---

### ✅ Option 3: Use `screen` (older alternative to `tmux`)

```bash
screen -S myprocess
```

Then run your command and press `Ctrl+A`, then `D` to detach.

---

Let me know which method you'd prefer, or if you want help installing `tmux` or `screen`.
✅ If you're inside a screen session:
You can gracefully terminate it by:

1. Exit the shell inside screen:
bash

exit
2. Or use the keyboard shortcut:
bash

Ctrl + D
This will terminate the shell in the screen session, effectively ending it.

✅ If you're outside the session:
First, list all screen sessions:

```bash
screen -ls
```
Example output:
```
csharp

There is a screen on:
    12345.myprocess (Detached)
Then kill the session by its ID:
```
```bash
screen -X -S 12345.myprocess quit
```
Or if you know just the ID:

```bash
screen -X -S 12345 quit
```
==================================================================
# To check **running background sessions or processes** that you've started on a remote server (via `nohup`, `tmux`, or `screen`), here’s how you can do it:

---

### 🔍 1. **Check Running `tmux` Sessions**

```bash
tmux ls
```

This will list all active `tmux` sessions. Example output:

```
mysession: 1 windows (created Wed May 15 10:00:00 2025)
```

---

### 🔍 2. **Check Running `screen` Sessions**

```bash
screen -ls
```

Example output:

```
There is a screen on:
    12345.myprocess (Detached)
1 Socket in /run/screen/S-yourusername.
```

---

### 🔍 3. **Check `nohup` Processes**

You can check for processes started with `nohup` using `ps` or `pgrep`. For example:

```bash
ps aux | grep python
```

Or more generally:

```bash
ps aux | grep nohup
```

You might see something like:

```
ubuntu   4567  0.1  1.2 123456 7890 ?   S   10:30   0:00 python your_script.py
```

Or check for all backgrounded jobs you started in the session:

```bash
jobs
```

---

Let me know what you're trying to monitor specifically, and I can tailor a command for that.
