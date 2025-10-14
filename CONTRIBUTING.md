# Contributing to Prompt Cookbook CLI 🎉

Thank you for your interest in contributing! We’re excited to have you join the Hacktoberfest fun and help improve this project.

---

## 🚀 1. Setup (Development)

1. **Fork & Clone the Repository**
   ```bash
   git clone https://github.com/your-username/prompt-cookbook-cli.git
   cd prompt-cookbook-cli
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Then, edit `.env` and fill in your API keys (e.g. `OPENAI_API_KEY`, `GROQ_API_KEY`).

5. **Run a Quick Test**
   ```bash
   python cli.py list
   ```
   or
   ```bash
   python cli.py run --task summarization --type article-summarization --input "Hello world"
   ```

---

## 🧩 2. How to Contribute

1. **Find or Create an Issue**
   - Look for issues labeled `good first issue`, `hacktoberfest`, or `help wanted`.
   - You can also open your own issue for bugs or feature suggestions.

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Add or modify code, tests, or documentation.
   - Make sure the project runs successfully after your changes.

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add feature: your short description"
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Go to your forked repo on GitHub → *Compare & Pull Request*.
   - Describe your changes clearly.
   - Link the issue it resolves (e.g. `Fixes #12`).

6. **Review and Merge**
   - Maintainers will review your PR.
   - Once approved, it’ll be merged into `main`.

---

## 💡 3. Contribution Tips

- Keep PRs small and focused.  
- Use meaningful commit messages.  
- Follow existing code style and structure.  
- Test before submitting.  
- Be respectful and collaborative — open source thrives on kindness 🤝

---

🎯 **Happy Hacking and Happy Hacktoberfest!**
