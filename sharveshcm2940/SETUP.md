# Setup
1. Create a public repo named exactly `sharveshcm2940` and push everything in this folder to it.
2. Edit the CONFIG block at the top of `scripts/render_cards.py` (name, tagline, role, status).
3. Repo > Settings > Actions > General > Workflow permissions: set to "Read and write".
4. Actions tab > "Render README cards" > Run workflow. The cards are generated and committed.
5. If the fetch step fails on GraphQL, create a personal access token (public repo read access)
   and save it as a repo secret named `PROFILE_TOKEN`.

Local preview (no data needed):  SAMPLE=1 STATIC=1 python scripts/render_cards.py
Real data locally:  GH_TOKEN=... python scripts/fetch_data.py && python scripts/render_cards.py
Fonts are already in fonts/. To rebuild them: pip install fonttools && python scripts/make_fonts.py
