# RefactorIQ Test Project

Small Python repository for testing the RefactorIQ GitHub App pull request integration. The file `pricing.py` intentionally includes code smells (long parameter list, magic numbers, repeated discount logic, mixed responsibilities, branch-heavy logic). The code remains functional and has reproducible tests.

## Test locally (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```

Expected: **6 passed**. This runs local tests only; it does not contact GitHub or DIWO.

## Test GitHub App / DIWO connection

1. Push this folder to a new GitHub repository (do not push the ZIP itself).
2. Install your RefactorIQ-DIWO GitHub App on that repository. Subscribe to `pull_request` events, grant Checks write, and configure a signed HTTPS webhook pointing to your running DIWO backend's `/api/github/webhook`.
3. Ensure the DIWO backend is running, the webhook secret and private key are configured, the GitHub job database tables exist, and its background worker is running.
4. Create a new branch and edit `pricing.py` (even adding a harmless comment is enough). Commit and push it.
5. Open a Pull Request into `main` and check GitHub App delivery status and the PR's Checks tab.

For the current Milestone 1, expect a **RefactorIQ / DIWO** Check Run with a neutral `DIWO Connected` result. Real code smell detection from the PR requires Milestone 2 (PR-specific CUQA integration) and is not verified by local pytest.

To run DIWO locally, you must expose your local Flask backend to GitHub via an HTTPS tunnel and configure the resulting public URL in the GitHub App settings. Never expose DIWO private keys, webhook secrets, or Supabase service-role keys in this test repository.
