# Deploying to Hugging Face Spaces 🚀

Streamlit Cloud can sometimes struggle with large applications or file limits (`inotify`). Hugging Face Spaces is a robust alternative that runs Dockerized containers natively.

## Step 1: Create the Space

1.  Go to **[Hugging Face Spaces](https://huggingface.co/spaces)**.
2.  Click **"Create new Space"**.
3.  **Space Name**: `uzio-rag-assistant` (or similar).
4.  **License**: `MIT` (optional).
5.  **Select the Space SDK**: Choose **Streamlit**.
6.  **Space Hardware**: Keep it on **CPU Basic (Free)**.
7.  **Visibility**: Public or Private (your choice).
8.  Click **"Create Space"**.

## Step 2: Connect Code

1.  Once created, you will see instructions.
2.  We will **Sync** your existing GitHub repository.
3.  Go to **Settings** (in your new Space).
4.  Scroll to **"Git Operations"** or look for "Docker" / "Repository" settings.
    *   *Easier Method*: GitHub Actions or Direct Push.
    *   **Simplest Method for You**:
        1.  In your Space, click **"Files"** -> **"Add file"** -> **"Upload files"**.
        2.  Drag and drop all files from this folder (`app.py`, `requirements.txt`, `packages.txt`, `assets/`, `processed_data/`, etc.).
        3.  *Better yet*: Since you already pushed to GitHub, just connect your GitHub repo!

### Connecting GitHub (Recommended)
1.  Go to your Space **Settings**.
2.  Look for **"Code repository"** or **"Connect to GitHub"**.
3.  Authorize Hugging Face to access your expected repo: `shobhit73/uzio_rag_tt_ts`.
4.  It will start building automatically!

## Step 3: Add Secrets (Important!)

Your app needs the `GOOGLE_API_KEY`.

1.  In your Space, click on **Settings**.
2.  Scroll to the **"Variables and secrets"** section.
3.  Click **"New secret"**.
4.  **Name**: `GOOGLE_API_KEY`
5.  **Value**: (Paste your key from `.env`)
6.  Click **Save**.

## Step 4: Watch it Build

1.  Click on the **App** tab.
2.  You will see "Building...".
3.  If it says "Running", you are done!
4.  If the Index is missing, our **Self-Healing** code will automatically run and build it in about 2 minutes.
