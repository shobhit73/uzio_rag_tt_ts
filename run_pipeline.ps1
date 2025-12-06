Write-Host "Starting Multi-modal RAG Pipeline..."

Write-Host "`n[1/4] Extracting content from DOCX files..."
python extractor.py
if ($LASTEXITCODE -ne 0) { Write-Error "Extraction failed"; exit }

Write-Host "`n[2/4] Processing content (Image Captioning & Question Generation)..."
Write-Host "This step uses the API and might take some time depending on document size."
python processor.py
if ($LASTEXITCODE -ne 0) { Write-Error "Processing failed"; exit }

Write-Host "`n[3/4] Building Vector Index..."
python indexer.py
if ($LASTEXITCODE -ne 0) { Write-Error "Indexing failed"; exit }

Write-Host "`n[4/4] Launching Streamlit App..."
streamlit run app.py
